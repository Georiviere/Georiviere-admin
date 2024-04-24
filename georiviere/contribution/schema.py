from django.utils.translation import gettext as _

from . import models

# The json schema is summarized on :
# https://github.com/Georiviere/Georiviere-admin/issues/139
# Depending on the category and type of the contributions, some fields are available or not.
# Here is the generation of the json schema used by the website portal.
# The fields available depending on the type of contributions follow the documentation of jsonschema :
# https://json-schema.org/understanding-json-schema/reference/conditionals.html


def get_contribution_properties():
    """Feature properties as form initial data format (name / value)"""
    # TODO: Use directly field definition for type / title / max length
    results = {
        "name_author": {"type": "string", "title": _("Name author"), "maxLength": 128},
        "first_name_author": {
            "type": "string",
            "title": _("First name author"),
            "maxLength": 128,
        },
        "email_author": {"type": "string", "title": _("Email"), "format": "email"},
        "date_observation": {
            "type": "string",
            "title": _("Observation's date"),
            "format": "date",
        },
        "description": {"type": "string", "title": _("Description")},
        "category": {
            "type": "string",
            "title": _("Category"),
            # TODO: Loop on contribution one to one field to get all possibilities
            "enum": [
                models.ContributionQuantity._meta.verbose_name.title(),
                models.ContributionQuality._meta.verbose_name.title(),
                models.ContributionFaunaFlora._meta.verbose_name.title(),
                models.ContributionLandscapeElements._meta.verbose_name.title(),
                models.ContributionPotentialDamage._meta.verbose_name.title(),
            ],
        },
    }
    if models.SeverityType.objects.exists():
        results["severity"] = {
            "type": "string",
            "title": _("Severity"),
            "enum": list(models.SeverityType.objects.values_list("label", flat=True)),
        }
    return results


def get_landing(choices, meta):
    landing = {
        "if": {"properties": {"type": {"const": choices.LANDING.label}}},
        "then": {
            "properties": {
                "landing_type": {
                    "type": "string",
                    "title": meta.get_field(
                        "landing_type"
                    ).related_model._meta.verbose_name.capitalize(),
                    "enum": list(
                        models.LandingType.objects.values_list("label", flat=True)
                    ),
                }
            },
        },
    }
    return landing


def get_excessive_cutting_riparian_forest(choices, meta):
    excessive_cutting_riparian_forest = {
        "if": {
            "properties": {
                "type": {"const": choices.EXCESSIVE_CUTTING_RIPARIAN_FOREST.label}
            }
        },
        "then": {
            "properties": {
                "excessive_cutting_length": {
                    "type": "number",
                    "title": meta.get_field(
                        "excessive_cutting_length"
                    ).verbose_name.capitalize(),
                }
            },
        },
    }
    return excessive_cutting_riparian_forest


def get_disruptive_jam(choices, meta):
    disruptive_jam = {
        "if": {"properties": {"type": {"const": choices.DISRUPTIVE_JAM.label}}},
        "then": {
            "properties": {
                "jam_type": {
                    "type": "string",
                    "title": meta.get_field(
                        "jam_type"
                    ).related_model._meta.verbose_name.capitalize(),
                    "enum": list(
                        models.JamType.objects.values_list("label", flat=True)
                    ),
                }
            },
        },
    }
    return disruptive_jam


def get_bank_erosion(choices, meta):
    bank_erosion = {
        "if": {"properties": {"type": {"const": choices.BANK_EROSION.label}}},
        "then": {
            "properties": {
                "length_bank_erosion": {
                    "type": "string",
                    "title": meta.get_field(
                        "length_bank_erosion"
                    ).verbose_name.capitalize(),
                }
            },
        },
    }
    return bank_erosion


def get_river_bed_incision(choices, meta):
    river_bed_incision = {
        "if": {"properties": {"type": {"const": choices.RIVER_BED_INCISION.label}}},
        "then": {
            "properties": {
                "bank_height": {
                    "type": "string",
                    "title": meta.get_field("bank_height").verbose_name.capitalize(),
                }
            },
        },
    }
    return river_bed_incision


def get_fish_diseases(choices, meta):
    fish_diseases = {
        "if": {"properties": {"type": {"const": choices.FISH_DISEASES.label}}},
        "then": {
            "properties": {
                "disease_type": {
                    "type": "string",
                    "title": meta.get_field(
                        "disease_type"
                    ).related_model._meta.verbose_name.capitalize(),
                    "enum": list(
                        models.DiseaseType.objects.values_list("label", flat=True)
                    ),
                }
            },
        },
    }
    return fish_diseases


def get_fish_mortality(choices, meta):
    fish_mortality_property = {
        "number_death": {
            "type": "number",
            "title": meta.get_field("number_death").verbose_name.capitalize(),
        },
    }
    if models.DeadSpecies.objects.exists():
        fish_mortality_property["dead_species"] = {
            "type": "string",
            "title": _("Observed species"),
            "enum": list(models.DeadSpecies.objects.values_list("label", flat=True)),
        }
    fish_mortality = {
        "if": {"properties": {"type": {"const": choices.FISH_MORTALITY.label}}},
        "then": {"properties": fish_mortality_property},
    }
    return fish_mortality


def get_potentialdamage_condition():
    potential_damage_choices = models.ContributionPotentialDamage.TypeChoice
    meta_potential_damage = models.ContributionPotentialDamage._meta

    initial_condition = {
        "if": {
            "properties": {
                "category": {"const": meta_potential_damage.verbose_name.title()}
            }
        },
        "then": {
            "properties": {
                "type": {
                    "type": "string",
                    "title": meta_potential_damage.get_field(
                        "type"
                    ).verbose_name.title(),
                    "enum": list(potential_damage_choices.labels),
                }
            },
            "required": ["type"],
        },
    }

    conditions_each_type = [
        initial_condition,
        get_excessive_cutting_riparian_forest(
            potential_damage_choices, meta_potential_damage
        ),
        get_bank_erosion(potential_damage_choices, meta_potential_damage),
        get_river_bed_incision(potential_damage_choices, meta_potential_damage),
        get_fish_mortality(potential_damage_choices, meta_potential_damage),
    ]
    # 2 types in fish mortality

    if models.LandingType.objects.exists():
        conditions_each_type.append(
            get_landing(potential_damage_choices, meta_potential_damage)
        )
    if models.JamType.objects.exists():
        conditions_each_type.append(
            get_disruptive_jam(potential_damage_choices, meta_potential_damage)
        )
    if models.DiseaseType.objects.exists():
        conditions_each_type.append(
            get_fish_diseases(potential_damage_choices, meta_potential_damage)
        )

    return conditions_each_type


def get_invasive_species(choices, meta):
    invasive_species_property = {
        "home_area": {
            "type": "string",
            "title": meta.get_field("home_area").verbose_name.capitalize(),
        },
    }
    if models.InvasiveSpecies.objects.exists():
        invasive_species_property["invasive_species"] = {
            "type": "string",
            "title": _("Observed species"),
            "enum": list(
                models.InvasiveSpecies.objects.values_list("label", flat=True)
            ),
        }
    invasive_species = {
        "if": {"properties": {"type": {"const": choices.INVASIVE_SPECIES.label}}},
        "then": {"properties": invasive_species_property},
    }
    return invasive_species


def get_heritage_species(choices, meta):
    heritage_species_property = {
        "number_heritage_species": {
            "type": "number",
            "title": meta.get_field(
                "number_heritage_species"
            ).verbose_name.capitalize(),
        },
    }
    if models.HeritageSpecies.objects.exists():
        heritage_species_property["heritage_species"] = {
            "type": "string",
            "title": _("Observed species"),
            "enum": list(
                models.HeritageSpecies.objects.values_list("label", flat=True)
            ),
        }
    if models.HeritageObservation.objects.exists():
        heritage_species_property["heritage_observation"] = {
            "type": "string",
            "title": _("Observation type"),
            "enum": list(
                models.HeritageObservation.objects.values_list("label", flat=True)
            ),
        }
    heritage_species = {
        "if": {"properties": {"type": {"const": choices.HERITAGE_SPECIES.label}}},
        "then": {"properties": heritage_species_property},
    }
    return heritage_species


def get_fish_species(choices, meta):
    fish_species_property = {
        "number_fish_species": {
            "type": "number",
            "title": meta.get_field("number_fish_species").verbose_name.capitalize(),
        },
    }
    if models.FishSpecies.objects.exists():
        fish_species_property["fish_species"] = {
            "type": "string",
            "title": _("Observed species"),
            "enum": list(models.FishSpecies.objects.values_list("label", flat=True)),
        }
    fish_species = {
        "if": {"properties": {"type": {"const": choices.FISH_SPECIES.label}}},
        "then": {"properties": fish_species_property},
    }
    return fish_species


def get_faunaflora_condition():
    faunaflora_choices = models.ContributionFaunaFlora.TypeChoice
    meta_faunaflora = models.ContributionFaunaFlora._meta

    initial_condition = {
        "if": {
            "properties": {"category": {"const": meta_faunaflora.verbose_name.title()}}
        },
        "then": {
            "properties": {
                "type": {
                    "type": "string",
                    "title": meta_faunaflora.get_field("type").verbose_name.title(),
                    "enum": list(faunaflora_choices.labels),
                }
            },
            "required": ["type"],
        },
    }

    conditions_each_type = [
        initial_condition,
        get_invasive_species(faunaflora_choices, meta_faunaflora),
        get_heritage_species(faunaflora_choices, meta_faunaflora),
        get_fish_species(faunaflora_choices, meta_faunaflora),
    ]
    return conditions_each_type


def get_overflow(choices, meta):
    overflow = {
        "if": {"properties": {"type": {"const": choices.OVERFLOW.label}}},
        "then": {
            "properties": {
                "landmark": {
                    "type": "string",
                    "title": meta.get_field("landmark").verbose_name.capitalize(),
                },
            }
        },
    }
    return overflow


def get_quantity_condition():
    quantity_choices = models.ContributionQuantity.TypeChoice
    meta_quantity = models.ContributionQuantity._meta

    initial_condition = {
        "if": {
            "properties": {"category": {"const": meta_quantity.verbose_name.title()}}
        },
        "then": {
            "properties": {
                "type": {
                    "type": "string",
                    "title": meta_quantity.get_field("type").verbose_name.capitalize(),
                    "enum": list(quantity_choices.labels),
                }
            },
            "required": ["type"],
        },
    }

    conditions_each_type = [
        initial_condition,
        get_overflow(quantity_choices, meta_quantity),
    ]
    return conditions_each_type


def get_pollution(choices, meta):
    pollution_property = {}
    if models.NaturePollution.objects.exists():
        pollution_property["nature_pollution"] = {
            "type": "string",
            "title": meta.get_field(
                "nature_pollution"
            ).related_model._meta.verbose_name.capitalize(),
            "enum": list(
                models.NaturePollution.objects.values_list("label", flat=True)
            ),
        }
    if models.TypePollution.objects.exists():
        pollution_property["type_pollution"] = {
            "type": "string",
            "title": meta.get_field(
                "type_pollution"
            ).related_model._meta.verbose_name.capitalize(),
            "enum": list(models.TypePollution.objects.values_list("label", flat=True)),
        }
    pollution = {
        "if": {"properties": {"type": {"const": choices.POLLUTION.label}}},
        "then": {"properties": pollution_property},
    }
    return pollution


def get_quality_condition():
    quality_choices = models.ContributionQuality.TypeChoice
    meta_quality = models.ContributionQuality._meta

    initial_condition = {
        "if": {
            "properties": {"category": {"const": meta_quality.verbose_name.title()}}
        },
        "then": {
            "properties": {
                "type": {
                    "type": "string",
                    "title": meta_quality.get_field("type").verbose_name.title(),
                    "enum": list(quality_choices.labels),
                }
            },
            "required": ["type"],
        },
    }

    conditions_each_type = [
        initial_condition,
    ]
    if models.NaturePollution.objects.exists() or models.TypePollution.objects.exists():
        conditions_each_type.append(get_pollution(quality_choices, meta_quality))
    return conditions_each_type


def get_landscapeelements_condition():
    landscapeelements_choices = models.ContributionLandscapeElements.TypeChoice
    meta_landscapeelements = models.ContributionLandscapeElements._meta

    initial_condition = {
        "if": {
            "properties": {
                "category": {"const": meta_landscapeelements.verbose_name.title()}
            }
        },
        "then": {
            "properties": {
                "type": {
                    "type": "string",
                    "title": meta_landscapeelements.get_field(
                        "type"
                    ).verbose_name.title(),
                    "enum": list(landscapeelements_choices.labels),
                }
            },
            "required": ["type"],
        },
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
        "required": ["email_author", "date_observation", "category"],
        "properties": get_contribution_properties(),
        "allOf": get_contribution_allOf(),
    }
