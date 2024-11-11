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
            # Map the fields correctly as per your CSV structure
            voter = Voter(
                last_name=fields[1].strip(),
                first_name=fields[2].strip(),
                street_number=fields[3].strip(),
                street_name=fields[4].strip(),
                apartment_number=fields[5].strip() if fields[5].strip() else '',
                zip_code=int(fields[6].strip()),
                date_of_birth=fields[7].strip(),
                date_of_registration=fields[8].strip(),
                party_affiliation=fields[9].strip(),
                precinct_number=int(fields[10].strip()),
                v20state=fields[11].strip().upper() == 'TRUE',
                v21town=fields[12].strip().upper() == 'TRUE',
                v21primary=fields[13].strip().upper() == 'TRUE',
                v22general=fields[14].strip().upper() == 'TRUE',
                v23town=fields[15].strip().upper() == 'TRUE',
                voter_score=int(fields[16].strip())
            )
            voter.save()  # Save this instance to the database.
            print(f'Created result: {voter}')

        except Exception as e:
            print(f"Exception on {fields}: {e}")