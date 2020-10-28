# Notes on how to upgrade GCA
- upgrades from activator to sbt
- upgrade from play 2.3 to current version

# sbt dependency management

## Latest version
https://www.scala-sbt.org/1.x/docs/Library-Dependencies.html
https://www.scala-sbt.org/1.x/docs/Library-Management.html
https://www.scala-sbt.org/1.x/docs/Resolvers.html
https://www.scala-sbt.org/1.x/docs/Proxy-Repositories.html

## sbt 0.13
https://www.scala-sbt.org/0.13/docs/Resolvers.html
https://www.scala-sbt.org/0.13.0/docs/Detailed-Topics/Library-Management.html

## Articles
https://alvinalexander.com/scala/sbt-how-to-manage-project-dependencies-in-scala/
https://hub.packtpub.com/dependency-management-sbt/


// Remove outdated default repositories
// externalResolvers := Resolver.withDefaultResolvers(resolvers.value, mavenCentral = false)
// externalResolvers <<= resolvers map{ rs =>   Resolver.withDefaultResolvers(rs, mavenCentral = false) }
externalResolvers := Seq.empty


We are using scala, sbt as build tool, activator as outdated and discontinued build tool wrapper and play as a server framework.
all of the above are outdated by a couple of years. The dependency repositories for all of the above have already changed dramatically and required major hacks and research to build the current state.

The pure sbt build does not work - the required dependencies cannot be resolved. It is only a matter of time until
the while project can no longer be built unless we catch up with the current play framework build.

https://dl.bintray.com/typesafe/maven-releases
https://dl.bintray.com/sbt/sbt-plugin-releases/
