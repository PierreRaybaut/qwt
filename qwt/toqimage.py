# -*- coding: utf-8 -*-
#
# Copyright © 2014-2015 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see qwt/LICENSE for details)

from qwt.qt.QtGui import QImage

import numpy as np


def array_to_qimage(arr, copy=False):
    """Convert NumPy array to QImage object"""
    # https://gist.githubusercontent.com/smex/5287589/raw/toQImage.py
    if arr is None:
        return QImage()
    if len(arr.shape) not in (2, 3):
        raise NotImplementedError("Unsupported array shape %r" % arr.shape)
    data = arr.data
    ny, nx = arr.shape[:2]
    stride = arr.strides[0]  # bytes per line
    color_dim = None
    if len(arr.shape) == 3:
        color_dim = arr.shape[2]
    if arr.dtype == np.uint8:
        if color_dim is None:
            qimage = QImage(data, nx, ny, stride, QImage.Format_Indexed8)
#            qimage.setColorTable([qRgb(i, i, i) for i in range(256)])
            qimage.setNumColors(256)
        elif color_dim == 3:
            qimage = QImage(data, nx, ny, stride, QImage.Format_RGB888)
        elif color_dim == 4:
            qimage = QImage(data, nx, ny, stride, QImage.Format_ARGB32)
        else:
            raise TypeError("Invalid third axis dimension (%r)" % color_dim)
    elif arr.dtype == np.uint32:
        qimage = QImage(data, nx, ny, stride, QImage.Format_ARGB32)
    else:
        raise NotImplementedError("Unsupported array data type %r" % arr.dtype)
    if copy:
        return qimage.copy()
    return qimage
