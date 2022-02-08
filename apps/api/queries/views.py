import importlib
from io import BytesIO

from django.db.models import Prefetch, Count, Q
from django.http import HttpResponse
from xlsxwriter.workbook import Workbook

from rest_framework import generics
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.queries.permissions import ViewPermission
from apps.api.queries.serializers import CategorySerializer, ParamSerializer
from apps.queries.models import Category, Query, Param


class CategoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    ordering_fields = ['name']

    def get_queryset(self):
        ids = self.request.user.queries.values('id')
        return Category.objects\
            .prefetch_related(Prefetch('queries',
                                       queryset=Query.objects.filter(id__in=ids)))\
            .annotate(queries_count=Count('queries', filter=Q(queries__id__in=ids)))\
            .filter(queries_count__gt=0)


class ParamView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ViewPermission]
    serializer_class = ParamSerializer
    ordering_fields = ['name']

    def get_queryset(self):
        slug = self.kwargs.get('slug', '')
        return Param.objects.filter(query__slug=slug)


class QueryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ViewPermission]
    serializer_class = CategorySerializer
    ordering_fields = ['name']
    queryset = Query.objects.all()
    lookup_url_kwarg = 'slug'

    def retrieve(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', '')
        instance = Query.objects.filter(slug=slug).first()
        if instance:
            connect = importlib.import_module("apps.queries.connections." + instance.database.type).Connect(instance)
            result = connect.run(request)
            return Response(data=result)
        else:
            return Response({
                'status': 0,
                'error': 'Not Found'
            })

    @action(methods=['get'], detail=False, url_name='excel', url_path='excel',)
    def excel(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug', '')
        instance = Query.objects.filter(slug=slug).first()
        data = []
        if instance:
            instance.pagination = False
            connect = importlib.import_module("apps.queries.connections." + instance.database.type).Connect(instance)
            data = connect.run(request)['data']
        else:
            return Response({
                'status': 0,
                'error': 'Not Found'
            })

        output = BytesIO()

        book = Workbook(output)
        sheet = book.add_worksheet('DATA')
        i = 0
        for item in data:
            j = 0
            for key, value in item.items():
                if i == 0:
                    sheet.write(i, j, key.upper())
                sheet.write(i+1, j, value)
                j += 1
            i += 1
        book.close()

        # construct response
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename=" + instance.title + ".xlsx"
        return response
