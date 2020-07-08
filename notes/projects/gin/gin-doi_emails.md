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

- The description of the dataset, which should serve the purpose of a brief abstract, hasn't been entered. In the datacite.yml file in the repository, the description contains the text from the template instead.
- Since this dataset appears to be supplementing a publication, you can add it in the references even though it's not yet published, by adding the full citation to the "name" field, adding "IsSupplemenTo" to the reftype, and keeping the "id" field empty. We will list the citation on the page of your dataset and once it is published, you can update the metadata with the DOI and we will add the link to the dataset appropriately.

Please update your repository with these changes and let us know if you have any questions. Once you are happy with the changes, resubmit the request or reply to this email and we will continue with the registration.

Thank you and best regards,

[xyz]
G-Node
