"""
Everything about here is customized REST API.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as RESPONSE_CODE
from .models import Research, Datasets
from django.core.exceptions import ObjectDoesNotExist
from app.utils import pdf_extract as BERT

class AnalyzePaper(APIView):

    def get(self, request, id):

        for_analyzation = Research.objects.all().filter(id=str(id), reviewed=False)

        if len(for_analyzation) < 1:

            return Response(
                {"detail": "Record has been reviewed."},
                RESPONSE_CODE.HTTP_304_NOT_MODIFIED,
            )

        try:

            research_object = Research.objects.get(id=str(id))
            print(research_object.file_location)

            pdf_path = "media/" + str(research_object.file_location)
            text = BERT.extract_text_from_pdf(pdf_path)
            valid_phrases = BERT.extract_valid_phrases(text)
            texts = BERT.get_texts_and_synonyms(valid_phrases)

            for each_rows in texts:

                Datasets.objects.create(
                    title_id=research_object,
                    phrase=each_rows["original_sentence"],
                    similar_sample=each_rows["new_sentence"],
                    plagiarized=False,
                )

            Research.objects.all().filter(id = int(id)).update(reviewed = True)

        except ObjectDoesNotExist as e:

            return Response(
                {"detail": "Research ID is not existing."},
                RESPONSE_CODE.HTTP_404_NOT_FOUND,
            )
        
        

        return Response(
            {
                "detail": "Research has been analyzed, check the datasets to proofread each sentences/phrases for the model."
            },
            RESPONSE_CODE.HTTP_200_OK,
        )
