import csv

from django.http import HttpResponse
from django.utils import timezone

from FIT.models import Participant


class ExportCsvMixin:

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = ['No.']
        for field in meta.fields:
            if field.name == 'participant':
                [field_names.append(f.name) for f in Participant._meta.fields if f.name != 'id']
            elif field.name == 'id':
                continue
            else:
                field_names.append(field.name)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        num_row = 1
        for obj in queryset:
            row_content = [str(num_row)]
            for field in meta.fields:
                attr = getattr(obj, field.name)
                if isinstance(attr, Participant):
                    row_content += [getattr(attr, f.name) for f in attr._meta.fields if f.name != 'id']
                elif field.name == 'id':
                    continue
                else:
                    row_content.append(attr)
            writer.writerow(row_content)
            num_row += 1

        return response

    export_as_csv.short_description = "Export Selected"
