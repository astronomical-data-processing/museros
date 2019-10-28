package org.cnlab.service;

import org.apache.log4j.Logger;
import org.cnlab.common.QueryModel;
import org.cnlab.model.ImageModel;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
@Service("imageService")
public class ImageServiceImpl implements IImageService {
    private static final Logger logger = Logger.getLogger(ImageServiceImpl.class);

    @Resource(name = "imageDao")
    private org.cnlab.dao.IImageDao imageDao;

    @Override
    public List<ImageModel> queryImage(QueryModel queryModel) throws Exception {
        return imageDao.find("from ImageModel i",queryModel.currentPage,queryModel.pageSize);
    }

    @Override
    public long queryImageCount() {
        return imageDao.count(" select count(*) from ImageModel i");
    }

    @Override
    public ImageModel querySingleImage(String imageID) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("imageID", Integer.valueOf(imageID));
        return imageDao.get("from ImageModel i where i.imageID=:imageID", map);
    }
}
