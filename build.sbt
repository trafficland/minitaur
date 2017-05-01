import play.sbt.PlayScala
import play.sbt.routes.RoutesKeys._
import play.sbt.PlayImport._
import sbt._
import sbt.Keys._

val appName = "minotaur"
val appVersion = "0.0.1-SNAPSHOT".toReleaseFormat

lazy val minotaur = (project in file("."))
  .enablePlugins(PlayScala)
  .enablePlugins(StandardPluginSet)
  .settings(commonSettings)
  .settings(
    cancelable in Global := true,
    libraryDependencies ++= dependencies
  )

lazy val commonSettings = Seq(
  name := appName,
  scalaVersion := "2.11.8",
  version := appVersion
)

lazy val dependencies = Seq(
  "org.scalatest" %% "scalatest" % "3.0.1" % "test",
  "org.slf4j" % "slf4j-nop" % "1.7.0",
  "ch.qos.logback" % "logback-classic" % "1.1.3",
  "org.webjars" %% "webjars-play" % "2.5.0",
  "net.codingwell"  %%   "scala-guice"  %   "4.0.0"
)