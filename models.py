import os
import peewee as pw
import datetime
from peewee_validates import ModelValidator, StringField, validate_length, validate_required, validate_email, validate_not_empty
from playhouse.postgres_ext import PostgresqlExtDatabase

db = PostgresqlExtDatabase(os.getenv('DATABASE'), host= "localhost")

class BaseModel(pw.Model):
  created_at = pw.DateTimeField(default=datetime.datetime.now)
  updated_at = pw.DateTimeField(default=datetime.datetime.now)

  def save(self, *args, **kwargs):
    validator = type(self).CustomValidator(self)
    validator.validate()

    self.errors = validator.errors

    if len(self.errors) == 0:
      self.updated_at = datetime.datetime.now()
      return super(BaseModel, self).save(*args, **kwargs)
    else:
      return 0

  class Meta:
    database = db
    legacy_table_names = False

  class CustomValidator(ModelValidator):
    pass

class Store(BaseModel):
  name = pw.CharField(unique=True)
 
class Warehouse(BaseModel):
  store = pw.ForeignKeyField(Store, backref='warehouses')
  location = pw.TextField()

class Product(BaseModel):
  name = pw.CharField(index=True)
  description = pw.TextField()
  warehouse = pw.ForeignKeyField(Warehouse, backref='products')
  color = pw.CharField(null=True)