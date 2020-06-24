# Potential changes notes for current files

- g-node.1e7756.xml
  - strange funding reference (empty DFG award number after full DFG entry)

        <fundingReference>
          <funderName>DFG</funderName>
          <awardNumber>SFB889</awardNumber>
        </fundingReference>
        <fundingReference>
          <funderName>DFG</funderName>
          <awardNumber></awardNumber>
        </fundingReference>

- g-node.5a4628
  - typo in fundingReference (`Helth`): `<funderName>Kids Brain Helth Network</funderName>`

- g-node.5b08du
  - empty language tag
  - empty version tag

- g-node.6a0d94
  - typo in title (`fied`): `<title>Local fied potential dataset:...`

- g-node.7a5020
  - repeating subjects

        <subjects>
          <subject>delay discounting, win-stay, lose-switch, perseveration, reversal learning, perceptual uncertainty</subject>
          <subject>win-stay, lose-switch</subject>
          <subject>perseveration</subject>
          <subject>reversal learning</subject>
          <subject>perceptual uncertainty</subject>
        </subjects>

- g-node.9c0912
  - again as in the related DOI g-node.5a4628 above, typo in fundingReference (`Helth`): `<funderName>Kids Brain Helth Network</funderName>`

- g-node.57a01e
  - author contains an empty ORCID entry for creator `Dominiak, Sina E.`

- g-node.d9dd71
  - size is `0 B`

- g-node.e520bb
  - lower case authors name: `<creatorName>chen, xi</creatorName>`

- g-node.hnj28q
  - empty relatedIdentifiers tag
  - empty language tag
  - empty version tag
  - size `0 B`

- g-node.m9hpkr
  - empty language tag
  - empty version tag

- g-node.o1g64d
  - empty relatedIdentifiers tag
  - empty language tag
  - empty version tag
  - size `0 B`

- g-node.t6vbz9
  - empty language tag
  - empty version tag

- g-node.vd9c21
  - empty language tag
  - empty version tag

## ROR additions

ROR Questions:
- g-node.5a4628
  - current funderName: `Kids Brain Health Network` without awardNumber or funderIdentifier. No ROR id exists for this foundation; googling reveals, that the foundation it was formerly known as `NeuroDevNet` which has the ROR ID `https://ror.org/04r0s0t24`. Should I leave this one as is or add the `NeuroDevNet` ROR ID as ROR funderIdentifier? The external page link on ROR for NeuroDevNet is dead btw.

- g-node.aa605a: contains a Crossref Funder ID (Seventh Framework Programme) that has no ROR, so I left it as is.

- g-node.f83565: contains a Crossref Funder ID (10.13039/100010664) that has no ROR, so I left it as is.

### ROR mappings
      <funderIdentifier funderIdentifierType="ROR">https://ror.org/04pz7b180</funderIdentifier>

https://ror.org/04pz7b180   BMBF
https://ror.org/018mejw64   DFG
https://ror.org/0472cxd90   ERC (European Research Council)
https://ror.org/00yjd3n13   SNSF (Swiss National Science Foundation)
https://ror.org/04s64z252   ICEMED
https://ror.org/021nxhr62   NSF (National science foundation)
https://ror.org/01cwqze88   NIH (National institutes of health)
https://ror.org/02jzrsm59   NIAAA
https://ror.org/05nzwyq50   JPB foundation
https://ror.org/03s0fv852   Einstein Stiftung
https://ror.org/03s0fv852   Einstein Foundation
https://ror.org/00rb16m44   Ministry of Human Capacities Hungary
https://ror.org/02ks8qq67   Hungarian Academy of Sciences
https://ror.org/03g2am276   National Research, Development and Innovation Office Hungary
https://ror.org/02ebx7v45   Human Frontiers Science Program
https://ror.org/03bsmfz84   Volkswagen Foundation
https://ror.org/02s016q17   Naito Foundation
https://ror.org/00gc20a07   Uehara Memorial Foundation
https://ror.org/05ar5fy68   Innovate UK
https://ror.org/0252rqe04   International Anesthesia Research Society
https://ror.org/04mhx6838   National Institute on Deafness and Other Communication Disorders
https://ror.org/00dkye506   Boehringer Ingelheim Fonds
https://ror.org/039djdh30   DAAD
https://ror.org/0281dp749   Helmholtz Association
https://ror.org/02feahw73   CNRS
https://ror.org/0210rze73   Stavros Niarchos Foundation

DOI link
    <relatedIdentifier relatedIdentifierType="DOI" relationType="IsSupplementTo"></relatedIdentifier>


## Update DOI links

Generally I added DOIs of full publications as relatedIdentifier DOI relationType="IsSupplementTo" if our DOI dataset was linked in the paper as "supplement" or data "availability". If our DOI dataset was not linked in the paper I chose relatedIdentifier DOI relationType="IsDescribedBy".

- g-node.6d38c0
  This seems to be data for the following paper: https://doi.org/10.1371/journal.pone.0223702
  It is not mentioned in the description though, one author on the paper is different, the paper title has changed as well and the gin doi is not in the paper.

- g-node.3730d0
  This seems to be data for the following paper: https://doi.org/10.1038/s41467-019-10428-1
  The gin doi is not mentioned anywhere.

- g-node.af468c: https://onlinelibrary.wiley.com/doi/full/10.1002/brb3.1155
  authors of the dataset and the paper are identical, the titel varies slightly and the gin doi is not mentioned in the paper.

- g-node.hnj28q: https://doi.org/10.1177/2041669517701458
  old dataset, does not mention g-node as hosting institution in the paper 

    - ~~g-node.2e31e3~~
    - ~~g-node.4bdb22~~
    - ~~g-node.5a4628~~
    - ~~g-node.7a5020~~
    - ~~g-node.8d6e59~~
    - ~~g-node.9c0912~~
    - ~~g-node.50baa6~~
    - ~~g-node.80dd9a~~
    - ~~g-node.85d46c~~
    - ~~g-node.91a992~~
    - ~~g-node.230a07~~
    - ~~g-node.298ce0~~
    - ~~g-node.0300fd~~
    - ~~g-node.3730d0~~
    - ~~g-node.4160bc~~
    - ~~g-node.6521de~~
    - ~~g-node.08853e~~
    - ~~g-node.10246f~~
    - ~~g-node.52349d~~
    - ~~g-node.92538d~~
    - ~~g-node.af468c~~
    - ~~g-node.b6d000~~
    - ~~g-node.b56be0~~
    - ~~g-node.b64563~~
    - ~~g-node.ec6518~~
    - ~~g-node.f13e77~~
    - ~~g-node.f93a29~~
    - ~~g-node.fb5bd5~~
    - ~~g-node.hnj28q~~
    - ~~g-node.o1g64d~~
