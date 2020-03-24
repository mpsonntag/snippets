
# concepts 

## format: Section type handling
- currently we have section type defined as a required attribute in format
- so far we have not checked the format required attributes. we now have a prototype validation that does this. I would like to remove some of the hard checks that are still in various code places.
- specifically we have not checked section type until now. now that we check for required attributes. If we keep this, we could render a lot of existing files that have not specified 'type' unsaveable since this is now an error.
- we could have a workaround e.g. render the required format validation as a mere warning for now, add a deprecation warning and switch to error in a couple of releases.
- further there is a difference between how a section is created from a sectionable and how it is normally initialized: by default it assigns type='undefined'.
  - section init and create_section should behave the same
  - I really don't like 'undefined'. If we keep it, should we switch to something else e.g. 'n/a'?

- should we also keep a release list to keep track of all the deprecated things we have lying around to remember to actually remove them after a couple of releases? Maybe as an own section in the README and documentation so people can see which features will be removed at which point in time? would that be a nice scheme?
 -> generally a good and accepted idea! have its own file -> deprecations.md and link prominently from the readme and documentation.

# new features

## container sections
- Add a clone_empty multiple times to a section; will be added to the parent section, name and type will stay the same, only the counter in name will go up. all properties will also be cloned but with empty values, units etc?
 - define
- add a clone child section to section, hand over a specific child section e.g. by name or id and clone it empty multiple times
- write a container section description in the tutorial.

## validations
- should we add a validation object to every loaded document in the first place? display an info to the user on load and hint to where the warnings and infos can be found?
- should the "this value is string but could be xy" warning be a new category: info?

- if we had dedicated container sections, we could check all direct child sections for consistency of name, type, properties, etc.

- maybe we should have different default validations on startup checks and when saving
  - the 'different dtype' validation might make sense when reading a file in - there could be data entry errors, but it could be very tedious seeing these warnings every time a file is saved or validated.

