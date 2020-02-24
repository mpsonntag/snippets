------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

userdash.js and abstracts-favourites.js
    // probably unused code
    self.makeAbstractLink = function (abstract, conference) {
        return "/myabstracts/" + abstract.uuid + "/edit";
    };

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

admin-conference.js

einige self.setErrors die man besser / anders mit setInfo und "Error" lösen kann.


favouriteAbstracts.scala

    <div class="panel-heading" >
        <div class="col-md-1">
            <a data-bind="attr: { href: link }">
                <span class="glyphicon glyphicon-home"></span>
            </a>
        </div>
        <div>
        <a data-bind="attr: { href: localConferenceLink() }">
            <h4 class="panel-title" data-bind="text: name"></h4>
        </a>
        </div>
    </div>

Editor

    self.doEndEdit = function () {
        console.log("Stop an edit")

        if (self.message() !== undefined && self.message() !== null) {
            console.log("we have a message: "+ self.message().message + " | " + self.message().desc)
        }

message

    self.clearMessage = function() {
        if (self.message() !== undefined && self.message() !== null) {
            console.log("clear message: "+ self.message().message)
        }
        self.message(null);
    };

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------

GCA-Web play migration 2.3 -> 2.4

/projects/plugins.sbt

    addSbtPlugin("com.typesafe.play" % "sbt-plugin" % "2.3.10")
change to 
    addSbtPlugin("com.typesafe.play" % "sbt-plugin" % "2.4.0")


/project/build.properties

    sbt.version=0.13.5
change to
    sbt.version=0.13.8


/build.sbt

    libraryDependencies
change to
    libraryDependencies ++= Seq(
      jdbc,
      cache,
      ws,
      "org.scalatest" %% "scalatest" % "2.2.1",
      "org.eclipse.persistence" % "org.eclipse.persistence.jpa" % "2.5.2",
      "com.typesafe.play" %% "anorm" % "2.4.0",
      "com.typesafe.play" %% "play-mailer" % "2.4.0",
      "com.mohiva" %% "play-silhouette" % "1.0",
      "com.sksamuel.scrimage" %% "scrimage-core" % "2.0.1",
      "org.postgresql" % "postgresql" % "9.3-1100-jdbc4",
      "com.atlassian.commonmark" % "commonmark" % "0.11.0",
      // web jars
      "org.webjars" % "requirejs" % "2.1.15",
      "org.webjars" % "jquery" % "1.11.2",
      "org.webjars" % "jquery-ui" % "1.11.2",
      "org.webjars" % "bootstrap" % "3.1.1" exclude("org.webjars", "jquery"),
      "org.webjars" % "knockout" % "3.0.0" exclude("org.webjars", "jquery"),
      "org.webjars" % "sammy" % "0.7.4",
      "org.webjars" % "momentjs" % "2.9.0",
      "com.googlecode.owasp-java-html-sanitizer" % "owasp-java-html-sanitizer" % "r136"
    )

------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------


