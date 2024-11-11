from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Voter
from django.db import models

from typing import Any
from django.shortcuts import render

import plotly
import plotly.graph_objects as go

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

class GraphsView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

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

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)

        # Filtering data for graphs
        voters = self.get_queryset()

        # Graph 1: Histogram of Voter distribution by Year of Birth
        birth_years = list(voters.values_list('date_of_birth__year', flat=True))
        histogram = go.Figure(
            data=[go.Histogram(x=birth_years, nbinsx=50, marker_color='blue')],
            layout=go.Layout(
                title='Voter Distribution by Year of Birth',
                xaxis=dict(title='Year of Birth'),
                yaxis=dict(title='Count')
            )
        )
        histogram_div = plotly.offline.plot(histogram, auto_open=False, output_type='div')
        context['histogram_div'] = histogram_div

        # Graph 2: Pie Chart of Voter distribution by Party Affiliation
        party_counts = voters.values('party_affiliation').annotate(count=models.Count('party_affiliation'))
        labels = [entry['party_affiliation'] for entry in party_counts]
        values = [entry['count'] for entry in party_counts]
        pie_chart = go.Figure(
            data=[go.Pie(labels=labels, values=values)],
            layout=go.Layout(title='Voter Distribution by Party Affiliation')
        )
        pie_chart_div = plotly.offline.plot(pie_chart, auto_open=False, output_type='div')
        context['pie_chart_div'] = pie_chart_div

        # Graph 3: Histogram of Voter Participation in Elections
        elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        election_counts = [voters.filter(**{election: True}).count() for election in elections]
        election_histogram = go.Figure(
            data=[go.Bar(x=elections, y=election_counts, marker_color='blue')],
            layout=go.Layout(
                title='Vote Count by Election',
                xaxis=dict(title='Election'),
                yaxis=dict(title='Count')
            )
        )
        election_histogram_div = plotly.offline.plot(election_histogram, auto_open=False, output_type='div')
        context['election_histogram_div'] = election_histogram_div

        # Add form data for filtering
        context['voter_scores'] = [0, 1, 2, 3, 4, 5]
        context['birth_years'] = list(range(1920, 2005))
        return context