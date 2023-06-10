from django.conf import settings
import os
import pandas as pd
from django.http import HttpResponse


def export_to_excel(serializer_data, filename):
    """
    Export the given serializer data to an Excel file with the given filename.

    Args:
        serializer_data: The data to export, as a list of dictionaries or a single dictionary.
        filename: The name to give the exported file.

    Returns:
        A tuple containing the HTTP response and the URL of the exported file.
    """
    # Convert the serializer data to a list of dictionaries
    if isinstance(serializer_data, list):
        data = [dict(d) for d in serializer_data]
    else:
        data = [dict(serializer_data)]

    # Create a DataFrame from the list of dictionaries
    data_frame = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
    file_path = os.path.join(settings.MEDIA_ROOT, f'{filename}.xlsx')
    data_frame.to_excel(file_path, sheet_name='Data', index=False)

    # Create the response
    with open(file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'

    # Construct the URL of the file
    file_url = settings.MEDIA_URL + f'{filename}.xlsx'

    # Return the response and URL
    return response, file_url
