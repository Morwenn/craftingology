# -*- coding: utf-8 -*-

# Copyright (c) 2021-2024 Morwenn
# SPDX-License-Identifier: BSL-1.0

import sys

import owlready2


# Create world and ontology
owlready2.default_world.set_backend(filename=sys.argv[1])
crafting = owlready2.get_ontology("http://morwenn.bzh/crafting.owl")

with crafting:

    class link(owlready2.DataProperty, owlready2.FunctionalProperty):
        """
        A link can be attached to any entity for additional explanations.
        """
        domain = [owlready2.Thing]
        range = [str]

    ##################################################
    # Provider

    class Provider(owlready2.Thing):
        pass

    class supergroups(Provider >> Provider):
        pass

    ##################################################
    # Product

    class Product(Provider):
        pass

    class description(owlready2.DataProperty, owlready2.FunctionalProperty):
        domain = [Product]
        range = [str]

    class provides(Provider >> Product):
        """
        This one is for products that can be trivially extracted
        from plants to provide an ingredient, without having to
        go through a recipe.

        For example an egg can provide egg white and egg yolk by
        simple separation, without any other ingredient nor tool,
        so we can avoid having to write a recipe for that.
        """

    class is_provided_by(Product >> Provider):
        inverse_property = provides

    ##################################################
    # Living organism

    class Organism(Provider):
        """
        Any taxon used to represent living organism.
        """

    class IUCN(owlready2.Datatype):
        """
        IUCN conservation status.
        """
        equivalent_to = [owlready2.OneOf([
            "EX",
            "EW",
            "CR",
            "EN",
            "VU",
            "NT",
            "CD",
            "LC",
            "DD",
            "NE",
        ])]

    class conservation_status(owlready2.DataProperty, owlready2.FunctionalProperty):
        """
        IUCN conversation status of an organism.
        """
        domain = [Organism]
        range = [IUCN]

    class is_protected(owlready2.DataProperty, owlready2.FunctionalProperty):
        """
        Whether an organism is locally protected by law. This information
        applies based on the location of the observation database.
        """
        domain = [Organism]
        range = [bool]

    class is_somewhat_edible(owlready2.DataProperty, owlready2.FunctionalProperty):
        """
        Whether some parts of the organism, whether raw or processed,
        are edible and can be used in the kitchen.
        """
        domain = [Organism]
        range = [bool]

    ##################################################
    # Kingdoms

    class Plant(Organism):
        """
        Plants are a type of provider identified by their binomial name.
        They generally provide ingredients under their common name.
        """

    class EEE(owlready2.Datatype):
        """
        Categories of invasive species (EEE = Espèces Exotiques Envahissantes).
        """
        equivalent_to = [owlready2.OneOf([
            "IA1", "IA2", "IA3",
            "IP1", "IP2", "IP3", "IP4", "IP5",
            "AS1", "AS2", "AS3", "AS4", "AS5", "AS6",
        ])]

    class invasiveness_status(owlready2.DataProperty, owlready2.FunctionalProperty):
        """
        EEE status of a vascular plant.
        """
        domain = [Plant]
        range = [EEE]

    class Fungus(Organism):
        """
        Fungus are a type of provider identified by their binomial name.
        Aerial parts of mushrooms, under their common names, can appear
        as ingredient.
        """

    class Animal(Organism):
        """
        Animals are a type of provider identified by their binomial name.
        """

    class Mycetozoa(Organism):
        """
        Mycetozoa are a type of provider identified by their binomial name.
        Some of them can be used as ingredients.
        """

    ##################################################
    # Ingredient

    class Ingredient(Product):
        """
        Ingredients are products that will be consumed by recipes
        and are not expected to remain once the recipe is done.
        """

    ##################################################
    # Tool

    class Tool(Product):
        """
        Tools are pretty self-explanatory: a recipe can use tools
        to make new products, but they are not expect to disappear
        one the recipe is done. They are also products because it
        is totally possible towrite a recipe to create new tools.
        """

    ##################################################
    # Recipe

    class Recipe(owlready2.Thing):
        """
        A recipe uses ingredients and tools to produce new products.
        The ingredients are consumed and should disappear by the time
        the recipe is done, while tools remain.

        The ontology is designed in such a way that several recipes
        can use similar ingredients to produce similar products.
        Supporting such redundancy is a feature.
        """

    class uses(Recipe >> Product):
        pass

    class is_used_by(Product >> Recipe):
        inverse_property = uses

    class produces(Recipe >> Product):
        pass

    class is_produced_by(Product >> Recipe):
        inverse_property = produces

    class text(owlready2.DataProperty, owlready2.FunctionalProperty):
        domain = [Recipe]
        range = [str]


crafting.save(file="crafting.owl", format="rdfxml")
owlready2.default_world.save()
