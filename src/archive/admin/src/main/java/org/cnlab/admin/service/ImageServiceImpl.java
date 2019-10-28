package org.cnlab.admin.service;

import org.apache.log4j.Logger;
import org.cnlab.admin.model.ImageModel;
import org.cnlab.common.Constants;
import org.cnlab.common.QueryModel;
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
    private static final Logger logger = Logger.getLogger(LoginServiceImpl.class);

    @Resource(name = "imageDao")
    private org.cnlab.admin.dao.IImageDao imageDao;
    /**
     * 0* @param imageModel
     *
     * @param imageModel
     * @return
     */
    @Override
    public void save(ImageModel imageModel) throws Exception {
        try {
            imageDao.save(imageModel);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public void update(ImageModel imageModel) throws Exception {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("name", imageModel.getName());
        map.put("imageID", imageModel.getImageID());
        try {
            imageDao.executeHQL("update ImageModel u set u.imageName=:imageName,u.name=:name,u.modifiedTime=:modifiedTime where u.imageID=:imageID",map);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public void delete(ImageModel imageModel) throws Exception {
        try {
            imageDao.delete(imageModel);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public List<ImageModel> queryImages(QueryModel queryModel) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("imageName", Constants.SUPERADMIN);
        return imageDao.find("from ImageModel u where u.imageName !=:imageName",map,queryModel.currentPage,queryModel.pageSize);
    }

    @Override
    public long queryAllImageCounts() {
        return imageDao.count(" select count(*) from ImageModel");
    }
}
