from django.db import models


class sui_api(models.Model):
    sr_no = models.BigIntegerField(primary_key=True)
    DPIIT = models.CharField(max_length=500, blank=True, null=True)
    companyName  = models.CharField(max_length=500, blank=True, null=True)
    stage= models.CharField(max_length=500, blank=True, null=True)
    focusIndustry  = models.CharField(max_length=500, blank=True, null=True)
    focusSector= models.CharField(max_length=500, blank=True, null=True)
    serviceArea  = models.CharField(max_length=5000, blank=True, null=True)
    location= models.CharField(max_length=500, blank=True, null=True)
    noOfYear  = models.CharField(max_length=10, blank=True, null=True)
    companyURL= models.CharField(max_length=500, blank=True, null=True)
    aboutDetails  = models.TextField(blank=True, null=True)
    joinedDate= models.CharField(max_length=500, blank=True, null=True)
    DPIITRecognised  = models.CharField(max_length=500, blank=True, null=True)
    activeSince= models.CharField(max_length=500, blank=True, null=True)
    pageurl =models.CharField(max_length=500, blank=True, null=True)
    Updated_date =models.CharField(max_length=500, blank=True, null=True)
    dipp_number= models.CharField(max_length=500, blank=True, null=True)
    legalName= models.CharField(max_length=500, blank=True, null=True)
    cin= models.CharField(max_length=500, blank=True, null=True)
    pan= models.CharField(max_length=500, blank=True, null=True)
    company_availability_status= models.CharField(max_length=500, blank=True, null=True)
    dateofScrapping= models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table='sui_final'
    