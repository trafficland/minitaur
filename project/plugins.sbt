resolvers ++= Seq(
  Resolver.url("bintray-trafficland-sbt-plugins", url("https://dl.bintray.com/trafficland/sbt-plugins/"))(
    Patterns(isMavenCompatible = false, Resolver.localBasePattern)
  )
)

addSbtPlugin("com.trafficland" % "augmentsbt" % "1.1.0")

addSbtPlugin("org.scalariform" % "sbt-scalariform" % "1.6.0")

addSbtPlugin("me.lessis" % "bintray-sbt" % "0.3.0")

addSbtPlugin("com.typesafe.play" % "sbt-plugin" % "2.5.9")