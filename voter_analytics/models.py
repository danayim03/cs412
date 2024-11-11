from django.db import models

class Voter(models.Model):
    # Basic Information
    first_name = models.TextField()
    last_name = models.TextField()
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()

    # Address Information
    street_number = models.TextField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.IntegerField()

    # Voting Information
    party_affiliation = models.TextField()
    precinct_number = models.IntegerField()

    # Voting Participation in Recent Elections
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Precinct: {self.precinct_number}, Score: {self.voter_score})"

def load_data():
    '''Load data records from a CSV file into Voter model instances.'''
    
    # Delete all records to clear out the database:
    Voter.objects.all().delete()
    
    # Path to the CSV file
    filename = '/Users/danayim/Desktop/Fall2024/CS412/newton_voters.csv'  # Update this path
    
    f = open(filename)
    headers = f.readline()
    print(headers)
        
    for line in f:
        try:
            fields = line.split(',')
            # Create a new Voter object using the data from the fields
            voter = Voter(
                first_name=fields[1],
                last_name=fields[0],
                date_of_birth=fields[6],
                date_of_registration=fields[7],
                street_number=fields[2],
                street_name=fields[3],
                apartment_number=fields[4] if fields[4] else '',
                zip_code=int(fields[5]),
                party_affiliation=fields[8],
                precinct_number=int(fields[9]),
                v20state=fields[10].strip().lower() == 'true',
                v21town=fields[11].strip().lower() == 'true',
                v21primary=fields[12].strip().lower() == 'true',
                v22general=fields[13].strip().lower() == 'true',
                v23town=fields[14].strip().lower() == 'true',
                voter_score=int(fields[15].strip())
            )
            voter.save() # save this instance to the database.
            print(f'Created result: {voter}')

        except:
            print(f"Exception on {fields}")