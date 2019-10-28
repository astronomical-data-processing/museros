package org.cnlab.service;

import org.cnlab.common.QueryModel;
import org.cnlab.model.ImageModel;

import java.util.List;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
public interface IImageService {
    /**
     0* @param solarEventModel
     * @return
     */
    List<ImageModel> queryImage(QueryModel queryModel) throws Exception;

    long queryImageCount();

    ImageModel querySingleImage(String imageID);
}
