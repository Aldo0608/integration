from aiohttp import web

from custom_components.hacs.helpers.functions.logger import getLogger
from custom_components.hacs.helpers.functions.path_exsist import async_path_exsist
from custom_components.hacs.share import get_hacs


async def async_serve_category_file(request, requested_file):
    hacs = get_hacs()
    logger = getLogger("web.category")
    try:
        if requested_file.startswith("themes/"):
            servefile = f"{hacs.core.config_path}/{requested_file}"
        else:
            servefile = f"{hacs.core.config_path}/www/community/{requested_file}"

        if await async_path_exsist(servefile):
            logger.debug(f"Serving {requested_file} from {servefile}")
            response = web.FileResponse(servefile)
            if requested_file.startswith("themes/"):
                response.headers["Cache-Control"] = "public, max-age=2678400"
            else:
                response.headers["Cache-Control"] = "no-store, max-age=0"
                response.headers["Pragma"] = "no-store"
            return response
        else:
            logger.error(
                f"{request.remote} tried to request '{servefile}' but the file does not exist"
            )

    except (Exception, BaseException) as exception:
        logger.debug(
            f"there was an issue trying to serve {requested_file} - {exception}"
        )

    return web.Response(status=404)
