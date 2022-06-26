# -*- coding: utf-8 -*-

# Copyright (c) 2021 Morwenn
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
        pass

    class is_provided_by(Product >> Provider):
        inverse_property = provides

    ##################################################
    # Plant

    class Plant(Provider):
        """
        Plants are a type of provider identified by their Latin
        name. They generally provide ingredients under their
        common name.
        """
        pass

    class is_somewhat_edible(owlready2.DataProperty, owlready2.FunctionalProperty):
        """
        Whether some parts of the plant, whether raw or processed,
        are edible and can be used in the kitchen.
        """
        domain = [Plant]
        range = [bool]

    ##################################################
    # Animal

    class Animal(Provider):
        """
        Animals are a type of provider identified by their Latin name.
        """
        pass

    ##################################################
    # Ingredient

    class Ingredient(Product):
        """
        Ingredients are products that will be consumed by recipes
        and are not expected to remain once the recipe is done.
        """
        pass

    ##################################################
    # Tool

    class Tool(Product):
        """
        Tools are pretty self-explanatory: a recipe can use tools
        to make new products, but they are not expect to disappear
        one the recipe is done. They are also products because it
        is totally possible towrite a recipe to create new tools.
        """
        pass

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
        pass

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
