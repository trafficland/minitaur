package controllers

import javax.inject._

import play.api.Configuration
import play.api.mvc._
import play.api.i18n._
import utils.ConfigKeys

@Singleton
class IndexController @Inject() (
    val messagesApi: MessagesApi,
    implicit val wja: WebJarAssets,
    configuration: Configuration
) extends Controller with I18nSupport {

  def index = Action { implicit request =>
    // TODO: Handle the option correctly.
    Ok(views.html.index(configuration.getString(ConfigKeys.mapsUrl).get))
  }
}