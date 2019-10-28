package org.cnlab.admin.service;

import org.cnlab.admin.model.ImageModel;
import org.cnlab.common.QueryModel;

import java.util.List;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
public interface IImageService {
    /**
     0* @param userModel
     * @return
     */
    void save(ImageModel userModel) throws Exception;

    void update(ImageModel userModel) throws Exception;

    void delete(ImageModel userModel) throws Exception;

    List<ImageModel> queryImages(QueryModel queryModel);

    long queryAllImageCounts();
}
