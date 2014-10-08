"""
   Copyright 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'rtubiopa@calpoly.edu'

from rest_framework import permissions


class SafeMethodsOnlyPermission(permissions.BasePermission):
    """
    Only can access non-destructive methods (like GET and HEAD).
    """

    def has_permission(self, request, view):
        return self.has_object_permission(request, view)

    def has_object_permission(self, request, view, obj=None):
        return request.method in permissions.SAFE_METHODS


class AuthorCanEditPermission(SafeMethodsOnlyPermission):
    """
    Allow everyone to list or view, but only the other can modify existing
    instances.
    """

    def has_object_permission(self, request, view, obj=None):
        """
        Overriden method.
        This object returns 'true' whether the request has permission to access
        to this object or not.
        """
        if obj is None:
            can_edit = True
        else:
            can_edit = request.user == obj.author

        return can_edit or super(AuthorCanEditPermission, self)\
            .has_object_permission(request, view, obj)