from django.utils.translation import gettext as _

from georiviere.contribution.models import (ContributionQuantity, ContributionQuality,
                                            ContributionFaunaFlora, ContributionLandscapeElements,
                                            ContributionPotentialDamage, SeverityType,
                                            LandingType, JamType, DiseaseType, DeadSpecies,
                                            InvasiveSpecies, HeritageSpecies, HeritageObservation, FishSpecies,
                                            NaturePollution, TypePollution)

# The json schema is summarize on :
# https://github.com/Georiviere/Georiviere-admin/issues/139
# Depending of the category and type of the contributions, some fields are available or not.
# Here is the generation of the json schema used by the website portal.
# The fields available depending on the type of contributions follow the documentation of jsonschema :
# https://json-schema.org/understanding-json-schema/reference/conditionals.html


def get_contribution_properties():
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
    }
    }
    if SeverityType.objects.exists():
        results['severity'] = {
            'type': "string",
            'title': _('Severity'),
            'enum': list(SeverityType.objects.values_list('label', flat=True))
        }
    return results


def get_landing(choices, meta):
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
                        'enum': list(LandingType.objects.values_list('label', flat=True))
                    }
            },
        }
    }
    return landing


def get_excessive_cutting_riparian_forest(choices, meta):
    excessive_cutting_riparian_forest = {
        'if': {
            'properties': {
                'type': {'const': str(choices.EXCESSIVE_CUTTING_RIPARIAN_FOREST.label)}}
        },
        'then': {
            'properties': {
                'excessive_cutting_length':
                    {
                        'type': "number",
                        'title': str(meta.get_field(
                            'excessive_cutting_length').verbose_name.title()),
                    }
            },
        }
    }
    return excessive_cutting_riparian_forest


def get_disruptive_jam(choices, meta):
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


def get_bank_erosion(choices, meta):
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


def get_river_bed_incision(choices, meta):
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


def get_fish_diseases(choices, meta):
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
                        'enum': list(DiseaseType.objects.values_list('label', flat=True))
                    }
            },
        }
    }
    return fish_diseases


def get_fish_mortality(choices, meta):
    fish_mortality_property = {
        'number_death':
            {
                'type': "number",
                'title': str(meta.get_field(
                    'number_death').verbose_name.title())
            },
    }
    if DeadSpecies.objects.exists():
        fish_mortality_property['dead_species'] = {
            'type': "string",
            'title': str(meta.get_field(
                'dead_species').verbose_name.title()),
            'enum': list(DeadSpecies.objects.values_list('label', flat=True))
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


def get_potentialdamage_condition():
    potential_damage_choices = ContributionPotentialDamage.TypeChoice
    meta_potential_damage = ContributionPotentialDamage._meta

    initial_condition = {
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
        initial_condition,
        get_excessive_cutting_riparian_forest(potential_damage_choices,
                                              meta_potential_damage),
        get_bank_erosion(potential_damage_choices, meta_potential_damage),
        get_river_bed_incision(potential_damage_choices, meta_potential_damage),
        get_fish_mortality(potential_damage_choices, meta_potential_damage)
    ]
    # 2 types in fish mortality

    if LandingType.objects.exists():
        conditions_each_type.append(get_landing(potential_damage_choices, meta_potential_damage))
    if JamType.objects.exists():
        conditions_each_type.append(get_disruptive_jam(potential_damage_choices, meta_potential_damage))
    if DiseaseType.objects.exists():
        conditions_each_type.append(get_fish_diseases(potential_damage_choices, meta_potential_damage))

    return conditions_each_type


def get_invasive_species(choices, meta):
    invasive_species_property = {
        'home_area':
            {
                'type': "string",
                'title': str(meta.get_field(
                    'home_area').verbose_name.title())
            },
    }
    if InvasiveSpecies.objects.exists():
        invasive_species_property['invasive_species'] = {
            'type': "string",
            'title': str(meta.get_field(
                'invasive_species').verbose_name.title()),
            'enum': list(InvasiveSpecies.objects.values_list('label', flat=True))
        }
    invasive_species = {
        'if': {
            'properties': {
                'type': {
                    'const': str(choices.INVASIVE_SPECIES.label)}}
        },
        'then': {
            'properties': invasive_species_property
        }
    }
    return invasive_species


def get_heritage_species(choices, meta):
    heritage_species_property = {
        'number_heritage_species':
            {
                'type': "number",
                'title': str(meta.get_field(
                    'number_heritage_species').verbose_name.title())
            },
    }
    if HeritageSpecies.objects.exists():
        heritage_species_property['heritage_species'] = {
            'type': "string",
            'title': str(meta.get_field(
                'heritage_species').verbose_name.title()),
            'enum': list(HeritageSpecies.objects.values_list('label', flat=True))
        }
    if HeritageObservation.objects.exists():
        heritage_species_property['heritage_observation'] = {
            'type': "string",
            'title': str(meta.get_field(
                'heritage_observation').verbose_name.title()),
            'enum': list(HeritageObservation.objects.values_list('label', flat=True))
        }
    heritage_species = {
        'if': {
            'properties': {
                'type': {
                    'const': str(choices.HERITAGE_SPECIES.label)}}
        },
        'then': {
            'properties': heritage_species_property
        }
    }
    return heritage_species


def get_fish_species(choices, meta):
    fish_species_property = {
        'number_fish_species':
            {
                'type': "number",
                'title': str(meta.get_field(
                    'number_fish_species').verbose_name.title())
            },
    }
    if FishSpecies.objects.exists():
        fish_species_property['fish_species'] = {
            'type': "string",
            'title': str(meta.get_field(
                'fish_species').verbose_name.title()),
            'enum': list(FishSpecies.objects.values_list('label', flat=True))
        }
    fish_species = {
        'if': {
            'properties': {
                'type': {
                    'const': str(choices.FISH_SPECIES.label)}}
        },
        'then': {
            'properties': fish_species_property
        }
    }
    return fish_species


def get_faunaflora_condition():
    faunaflora_choices = ContributionFaunaFlora.TypeChoice
    meta_faunaflora = ContributionFaunaFlora._meta

    initial_condition = {
        'if': {
            'properties': {'category': {'const': str(meta_faunaflora.verbose_name.title())}}
        },
        'then': {
            'properties': {
                'type': {
                    'type': "string",
                    'title': str(meta_faunaflora.get_field('type').verbose_name.title()),
                    'enum': list(faunaflora_choices.labels)
                }
            },
            "required": ['type'],
        }
    }

    conditions_each_type = [
        initial_condition,
        get_invasive_species(faunaflora_choices, meta_faunaflora),
        get_heritage_species(faunaflora_choices, meta_faunaflora),
        get_fish_species(faunaflora_choices, meta_faunaflora)
    ]
    return conditions_each_type


def get_overflow(choices, meta):
    overflow = {
        'if': {
            'properties': {
                'type': {
                    'const': str(choices.OVERFLOW.label)}}
        },
        'then': {
            'properties': {
                'landmark':
                    {
                        'type': "string",
                        'title': str(meta.get_field(
                            'landmark').verbose_name.title())
                    },
            }
        }
    }
    return overflow


def get_quantity_condition():
    quantity_choices = ContributionQuantity.TypeChoice
    meta_quantity = ContributionQuantity._meta

    initial_condition = {
        'if': {
            'properties': {'category': {'const': str(meta_quantity.verbose_name.title())}}
        },
        'then': {
            'properties': {
                'type': {
                    'type': "string",
                    'title': str(meta_quantity.get_field('type').verbose_name.title()),
                    'enum': list(quantity_choices.labels)
                }
            },
            "required": ['type'],
        }
    }

    conditions_each_type = [
        initial_condition,
        get_overflow(quantity_choices, meta_quantity),
    ]
    return conditions_each_type


def get_pollution(choices, meta):
    pollution_property = {}
    if NaturePollution.objects.exists():
        pollution_property['nature_pollution'] = {
            'type': "string",
            'title': str(meta.get_field(
                'nature_pollution').verbose_name.title()),
            'enum': list(NaturePollution.objects.values_list('label', flat=True))
        }
    if TypePollution.objects.exists():
        pollution_property['type_pollution'] = {
            'type': "string",
            'title': str(meta.get_field(
                'type_pollution').verbose_name.title()),
            'enum': list(TypePollution.objects.values_list('label', flat=True))
        }
    pollution = {
        'if': {
            'properties': {
                'type': {
                    'const': str(choices.POLLUTION.label)}}
        },
        'then': {
            'properties': pollution_property
        }
    }
    return pollution


def get_quality_condition():
    quality_choices = ContributionQuality.TypeChoice
    meta_quality = ContributionQuality._meta

    initial_condition = {
        'if': {
            'properties': {'category': {'const': str(meta_quality.verbose_name.title())}}
        },
        'then': {
            'properties': {
                'type': {
                    'type': "string",
                    'title': str(meta_quality.get_field('type').verbose_name.title()),
                    'enum': list(quality_choices.labels)
                }
            },
            "required": ['type'],
        }
    }

    conditions_each_type = [
        initial_condition,

    ]
    if NaturePollution.objects.exists() or TypePollution.objects.exists():
        conditions_each_type.append(get_pollution(quality_choices, meta_quality))
    return conditions_each_type


def get_landscapeelements_condition():
    landscapeelements_choices = ContributionLandscapeElements.TypeChoice
    meta_landscapeelements = ContributionLandscapeElements._meta

    initial_condition = {
        'if': {
            'properties': {'category': {'const': str(meta_landscapeelements.verbose_name.title())}}
        },
        'then': {
            'properties': {
                'type': {
                    'type': "string",
                    'title': str(meta_landscapeelements.get_field('type').verbose_name.title()),
                    'enum': list(landscapeelements_choices.labels)
                }
            },
            "required": ['type'],
        }
    }

    conditions_each_type = [
        initial_condition,

    ]
    return conditions_each_type


def get_contribution_allOf():
    all_of_conditions = get_potentialdamage_condition()
    all_of_conditions += get_faunaflora_condition()
    all_of_conditions += get_quantity_condition()
    all_of_conditions += get_quality_condition()
    all_of_conditions += get_landscapeelements_condition()
    return all_of_conditions


def get_contribution_json_schema():
    return {
        "type": "object",
        "required": ['email_author', 'date_observation', 'category'],
        "properties": get_contribution_properties(),
        "allOf": get_contribution_allOf()
    }
