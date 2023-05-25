from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from georiviere.contribution.models import (Contribution, ContributionQuantity, ContributionQuality,
                                            ContributionFaunaFlora, ContributionLandscapeElements,
                                            ContributionPotentialDamage, SeverityType,
                                            LandingType, JamType, DiseaseType, DeadSpecies)
from django.utils.translation import gettext as _


class ContributionSerializer(serializers.Serializer):
    type = serializers.CharField(default='object')
    required = serializers.SerializerMethodField(method_name='get_required')
    properties = serializers.SerializerMethodField()
    allOf = serializers.SerializerMethodField()

    def get_required(self, obj):
        # TODO: Loop on fields to get required
        return ['email_author', 'date_observation', 'category']

    def get_properties(self, obj):
        """ Feature properties as form initial data format (name / value) """
        # TODO: Use directly field definition for type / title / max length
        results = {'name_author': {
            'type': "string",
            'title': _("Name author"),
            "maxLength": 128
        }, 'first_name_author': {
            'type': "string",
            'title': _("First name author"),
            "maxLength": 128
        }, 'email_author': {
            'type': "string",
            'title': _("Email"),
            'format': "email"
        }, 'date_observation': {
            'type': "string",
            'title': _("Observation's date"),
            'format': 'date'
        }, 'description': {
            'type': "string",
            'title': _('Description')
        }, 'category': {
            "type": "string",
            "title": _("Category"),
            # TODO: Loop on contribution one to one field to get all possibilities
            "enum": [
                str(ContributionQuantity._meta.verbose_name.title()),
                str(ContributionQuality._meta.verbose_name.title()),
                str(ContributionFaunaFlora._meta.verbose_name.title()),
                str(ContributionLandscapeElements._meta.verbose_name.title()),
                str(ContributionPotentialDamage._meta.verbose_name.title())
            ],
        },
        }
        if SeverityType.objects.exists():
            results['severity'] = {
                'type': "string",
                'title': _('Severity'),
                'enum': list(SeverityType.objects.all())
            }
        return results

    def get_landing(self, choices, meta):
        landing = {
            'if': {
                'properties': {'type': {'const': str(choices.LANDING.label)}}
            },
            'then': {
                'properties': {
                    'landing_type':
                        {
                            'type': "string",
                            'title': meta.get_field('landing_type').verbose_name.title(),
                            'enum': list(LandingType.objects.all())
                        }
                },
            }
        }
        return landing

    def get_excessive_cutting_riparian_forest(self, choices, meta):
        excessive_cutting_riparian_forest = {
            'if': {
                'properties': {
                    'type': {'const': str(choices.EXCESSIVE_CUTTING_RIPARIAN_FOREST.label)}}
            },
            'then': {
                'properties': {
                    'landing_type':
                        {
                            'type': "string",
                            'title': str(meta.get_field(
                                'landing_type').verbose_name.title()),
                        }
                },
            }
        }
        return excessive_cutting_riparian_forest

    def get_disruptive_jam(self, choices, meta):
        disruptive_jam = {
            'if': {
                'properties': {
                    'type': {
                        'const': str(choices.DISRUPTIVE_JAM.label)}}
            },
            'then': {
                'properties': {
                    'jam_type':
                        {
                            'type': "string",
                            'title': str(meta.get_field(
                                'jam_type').verbose_name.title()),
                        }
                },
            }
        }
        return disruptive_jam

    def get_bank_erosion(self, choices, meta):
        bank_erosion = {
            'if': {
                'properties': {
                    'type': {
                        'const': str(choices.BANK_EROSION.label)}}
            },
            'then': {
                'properties': {
                    'length_bank_erosion':
                        {
                            'type': "string",
                            'title': str(meta.get_field(
                                'length_bank_erosion').verbose_name.title()),
                        }
                },
            }
        }
        return bank_erosion

    def get_river_bed_incision(self, choices, meta):
        river_bed_incision = {
            'if': {
                'properties': {
                    'type': {
                        'const': str(choices.RIVER_BED_INCISION.label)}}
            },
            'then': {
                'properties': {
                    'bank_height':
                        {
                            'type': "string",
                            'title': str(meta.get_field(
                                'bank_height').verbose_name.title()),
                        }
                },
            }
        }
        return river_bed_incision

    def get_fish_diseases(self, choices, meta):
        fish_diseases = {
            'if': {
                'properties': {
                    'type': {
                        'const': str(choices.FISH_DISEASES.label)}}
            },
            'then': {
                'properties': {
                    'disease_type':
                        {
                            'type': "string",
                            'title': str(meta.get_field(
                                'disease_type').verbose_name.title()),
                            'enum': list(DiseaseType.objects.all())
                        }
                },
            }
        }
        return fish_diseases

    def get_fish_mortality(self, choices, meta):
        fish_mortality_property = {
            'number_death':
                {
                    'type': "string",
                    'title': str(meta.get_field(
                        'number_death').verbose_name.title())
                },
        }
        if DeadSpecies.objects.exists():
            fish_mortality_property['dead_species'] = {
                'type': "string",
                'title': str(meta.get_field(
                    'dead_species').verbose_name.title()),
                'enum': list(DeadSpecies.objects.all())
            }
        fish_mortality = {
            'if': {
                'properties': {
                    'type': {
                        'const': str(choices.FISH_MORTALITY.label)}}
            },
            'then': {
                'properties': fish_mortality_property
            }
        }
        return fish_mortality

    def get_potentialdamage_condition(self):
        potential_damage_choices = ContributionPotentialDamage.TypeChoice
        meta_potential_damage = ContributionPotentialDamage._meta

        inital_condition = {
            'if': {
                'properties': {'category': {'const': str(meta_potential_damage.verbose_name.title())}}
            },
            'then': {
                'properties': {
                    'type': {
                        'type': "string",
                        'title': str(meta_potential_damage.get_field('type').verbose_name.title()),
                        'enum': list(potential_damage_choices.labels)
                    }
                },
                "required": ['type'],
            }
        }

        conditions_each_type = [
            inital_condition,
            self.get_excessive_cutting_riparian_forest(potential_damage_choices,
                                                       meta_potential_damage),
            self.get_bank_erosion(potential_damage_choices, meta_potential_damage),
            self.get_river_bed_incision(potential_damage_choices, meta_potential_damage),
            self.get_fish_mortality(potential_damage_choices, meta_potential_damage)
        ]
        # 2 types in fish mortality

        if LandingType.objects.exists():
            conditions_each_type.append(self.get_landing(potential_damage_choices, meta_potential_damage))
        if JamType.objects.exists():
            conditions_each_type.append(self.get_disruptive_jam(potential_damage_choices, meta_potential_damage))
        if DiseaseType.objects.exists():
            conditions_each_type.append(self.get_fish_diseases(potential_damage_choices, meta_potential_damage))

        return conditions_each_type

    def get_allOf(self, obj):
        all_of_conditions = self.get_potentialdamage_condition()
        return all_of_conditions

    class Meta:
        geo_field = 'geom'
        fields = (
            'type', 'required', 'properties', 'allOf'
        )
