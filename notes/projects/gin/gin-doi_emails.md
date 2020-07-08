# GIN-DOI response email templates

## Missing license file

Dear [xyz],

We have received your request to register a new dataset from the GIN repository at https://gin.g-node.org/[xyz]. Before we can proceed with the publication, there is one issue that should be addressed:

1. There is no LICENSE file in the repository. While the datacite.yml specifies the license, we also require that the full text of the license is also included in the repository, which in turn is distributed with the dataset archive for any user that might obtain it.

Once this issue is resolved, please resubmit the request and we will proceed with the publication.

Thank you and best regards,

[xyz]
G-Node


## Missing datacite.yaml entries

Dear [xyz],

We have received your request to register the GIN repository at https://gin.g-node.org/[xyz].  Before we proceed with the registration, there are a few issues with the metadata that need to be addressed.

- The description section is the placeholder text from the template file. Please update this with a description of the dataset being registered? This can be a couple of sentences serving as a short, abstract-like description.

- Since this dataset appears to be supplementing a publication, you can add it in the references even though it's not yet published, by adding the full citation to the "name" field, adding "IsSupplemenTo" to the reftype, and keeping the "id" field empty. We will list the citation on the page of your dataset and once it is published, you can update the metadata with the DOI and we will add the link to the dataset appropriately.

- The "references" section contains some template text from the original datacite.yaml file. For the first reference, the DOI is 10.xxx/zzzz.  Additionally, the second reference is still template text. If there is no second reference, the second "reftype" and "name" can be safely removed. If the DOIs are not available yet, you can update them later in the datacite.yml and the README and we will pick up the changes and add them to the published metadata.

- The first author's information contains an ID field with value "AuthorID1 (e.g. ORCID)", which is the placeholder value from the datacite.yml template. Please either remove this placeholder text or update it with the proper ORCID if you have one.

Please update your repository with these changes and let us know if you have any questions. Once you are happy with the changes, resubmit the request or reply to this email and we will continue with the registration.

Thank you and best regards,

[xyz]
G-Node


## README character problems

Dear [xyz],

We have received your request to register the GIN repository at https://gin.g-node.org/[xyz]. Before we continue with the registration process, there are a few issues with the metadata and descriptions that should be addressed.

- The README.md file contains characters that do not appear to be unicode. This is preventing the website from displaying the README contents on the front page of the repository. Removing these characters (or replacing them if they are meant to be something else) should fix the problem.
- The description of the repository seems to have the same character issue as the README.md file. [point to character location]

Please make the appropriate changes and resubmit the registration request when everything is ready. We will then begin the registration process and inform you of the new DOI when it is ready.

Thank you and best regards,

[xyz]
G-Node


## Publication reference request

Dear [xyz],

Your dataset with title
[xyz]
has been successfully registered
The new DOI for the dataset is: [xyz] and can be viewed at https://doi.org/[xyz].

If this is data supplementing a publication and if you haven't done so already, we kindly request you to:
- Include the new DOI of this dataset and the DOI URL (not the repository URL) in the publication as a reference. Note that PLOS has a special Data Availability field for this particular purpose. Typically, this addition can be done as a request to changes in the proofs.
- Update the datacite file of the registered dataset to reference the publication, including its DOI, once it is known.

The latter will result in a link in the Datacite database to your publication and will increase its discoverability.

Thank you and best regards,

[xyz]
G-Node

