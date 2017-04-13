from api.models import BaseTag

TAGS = {
  'fairness': {
    'color': '#bcf0ff',
    'description': 'Fairness is ideas of justice, rights, and autonomy.',
  },
  'cheating': {
    'color': '#feffbc',
    'description': 'Cheating is acting dishonestly or unfairly in order to gain an advantage.',
  },
  'loyalty': {
    'color': '#bcffe2',
    'description': 'Loyalty underlies virtues of patriotism and self-sacrifice for the group.',
  },
  'betrayal': {
    'color': '#ffe5bc',
    'description': 'Betrayal is disloyalty and the destruction of trust.',
  },
  'care': {
    'color': '#bcc1ff',
    'description': 'Care is concern for the well-being of others.',
  },
  'harm': {
    'color': '#ffbcf5',
    'description': 'Harm is something that causes someone or something to be hurt, broken, made less valuable or successful, etc.',
  },
  'authority': {
    'color': '#ffb29e',
    'description': 'Authority underlies virtues of leadership and followership, including deference to legitimate authority and respect for traditions.',
  },
  'subversion': {
    'color' :'#e7bcff',
    'description': 'Subversion is the undermining of the power and authority of an established system or institution.',
  },
  'sanctity': {
    'color': '#d6ffbc',
    'description': 'Sanctity underlies notions of striving to live in an elevated, less carnal, more noble way.',
  },
  'degradation': {
    'color': '#ffbcd1',
    'description': 'Degradation is the process in which the beauty or quality of something is destroyed or spoiled',
  },
  'morality': {
    'color' : '#c1bfc0',
    'description': 'Morality is a particular system of values and principles of conduct.',
  },
};

def populate_base_tags(tags):
  for tag in tags:
    BaseTag.objects.get_or_create(
      name=tag, 
      color=tags[tag]["color"],
      description=tags[tag]["description"]
    )

  print "Base tags created!"

populate_base_tags(TAGS)