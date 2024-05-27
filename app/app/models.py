"""
Definition of models.
"""

from django.db import models
from app.utils import pdf_extract as BERT
from app.constants import app_constants
import json

class Config(models.Model):

    year = models.IntegerField()
    day = models.IntegerField()
    month = models.IntegerField()

class Credibility(models.Model):

    title = models.TextField(null=False, default="No Title")
    description = models.TextField(null=True, default="No Description / (N/A)")
    file_location = models.FileField(upload_to="reviewed_papers")
    plagiarism_level = models.FloatField(default=0.00)
    is_plagirized = models.BooleanField(default = False)

    remarks = models.TextField(default=None)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )  # Execute inherited default.

        self.analyze_saved_file()

    def analyze_saved_file(self):
        try:
            saved_text = self.get_saved_contents()
            self.get_paper_contents(saved_text)
        except Exception as e:
            print(e)
            Credibility.objects.all().filter(id = self.pk).delete()

    def get_saved_contents(self):
        self_instance = Credibility.objects.get(id=int(self.pk))
        pdf_path = "media/" + str(self_instance.file_location)
        text = BERT.extract_text_from_pdf(pdf_path)
        return text
  
        
    def get_paper_contents(self, text_contents: str) -> None:
        """Do a select query and join all so no CPU intensive will be done."""

        bert_instance = BERT.BERTAlgorithm()
        messages = []

        research_papers = Research.objects.all()
        if len(research_papers) > 0:
            total_mean = 0
            papers = 0
            for each_papers in research_papers:

                paper_contents = self.join_paper_contents(each_papers.pk)
                calculated_cosine = bert_instance.calculate_cosine(text_contents, paper_contents)
                
                total_mean = total_mean + calculated_cosine

                if calculated_cosine >= app_constants.ACCEPTABLE_PLAGIARISM_SENTENCES:

                    messages.append({
                        "title": each_papers.title,
                        "location": str(each_papers.file_location)
                    })

                papers = papers + 1 # Increment paper

            total_mean = total_mean / papers
            total_mean = round(total_mean, 2)


        plagiarized = False

        if calculated_cosine >= app_constants.ACCEPTABLE_PLAGIARISM_LEVEL:
            plagiarized = True

        Credibility.objects.all().filter(id = self.pk).update(
            plagiarism_level = total_mean, is_plagirized = plagiarized,
            remarks = json.dumps(messages)
        )

        print("Plagiarism level was updated.")
                

    def join_paper_contents(self, id: int) -> str:
        """
        Join all paper contents by research paper.
        args:
            id : primary key of research paper.

        returns:
            "" : if not found
        """

        placeholder = ""
        each_sentences = Datasets.objects.all().filter(title_id=int(id))

        if isinstance(id, int) == False or len(each_sentences) < 1:
            return ""

        if len(each_sentences) > 0:

            for sentence in each_sentences:
                placeholder = placeholder + sentence.phrase + " "
            else:
                placeholder = placeholder[0 : len(placeholder) - 1]

            return placeholder

class Research(models.Model):

    title = models.TextField(null=False, default="No Title")
    description = models.TextField(null=True, default="No Description / (N/A)")
    file_location = models.FileField(upload_to="papers")
    reviewed = models.BooleanField(default=False)


class Datasets(models.Model):

    title_id = models.ForeignKey(Research, on_delete=models.CASCADE)
    phrase = models.TextField(null=True)
    similar_sample = models.TextField(null=True)
    plagiarized = models.BooleanField(default=False)
