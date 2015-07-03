# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2015 Université Catholique de Louvain.
#
# This file is part of INGInious.
#
# INGInious is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INGInious is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with INGInious.  If not, see <http://www.gnu.org/licenses/>.
""" Authentication """

import web

from frontend.pages.api._api_page import APIPage, APIInvalidArguments
import frontend.user as User


class APIAuthentication(APIPage):
    """
        Endpoint /api/v0/authentication
    """

    def API_GET(self):
        """
            Returns {"status": "not authenticated"} or {"status": "authenticated", "username": "your_username"} (always 200 OK)
        """
        if User.is_logged_in():
            return 200, {"status": "authenticated", "username": User.get_username()}
        else:
            return 200, {"status": "not authenticated"}

    def API_POST(self):
        """
            Authenticates the remote client. Takes as input:

            auth_method_id
                an id for an auth method as returned be /api/v0/auth_methods

            input_key_1
                the first input key and its value

            input_key_2
                the first input key and its value

            ...
                ...

            Response: a dict in the form {"status": "success"} (200 OK) or {"status": "error"} (403 Forbidden)
        """

        user_input = web.input()
        if not "auth_method_id" in user_input:
            raise APIInvalidArguments()

        try:
            auth_method_id = int(user_input["auth_method_id"])
        except:
            raise APIInvalidArguments()

        del user_input["auth_method_id"]

        try:
            if User.connect(auth_method_id, dict(user_input)):
                return 200, {"status": "success"}
        except:
            pass
        return 403, {"status": "error"}
