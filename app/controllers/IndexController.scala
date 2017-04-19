package controllers

import javax.inject._
import play.api.mvc._
import play.api.i18n._

@Singleton
class IndexController @Inject() (
    val messagesApi: MessagesApi,
    implicit val wja: WebJarAssets
) extends Controller with I18nSupport {

  def index = Action { implicit request =>
    Ok(views.html.index())
  }
}