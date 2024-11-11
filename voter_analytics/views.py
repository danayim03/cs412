from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Voter

class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voters_list.html'
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()
        
        # Get filter values from the request
        party_affiliation = self.request.GET.get('party_affiliation')
        voter_score = self.request.GET.get('voter_score')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        
        # Apply filters if values are provided
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)
        
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
        
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
        
        # Checkboxes for election participation
        if self.request.GET.get('v20state'):
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town'):
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary'):
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general'):
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town'):
            queryset = queryset.filter(v23town=True)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['voter_scores'] = [0, 1, 2, 3, 4, 5]
        context['birth_years'] = list(range(1920, 2005))
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'