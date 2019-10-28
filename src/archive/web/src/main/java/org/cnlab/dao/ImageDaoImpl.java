package org.cnlab.dao;

import org.cnlab.common.dao.impl.BaseDaoImpl;
import org.cnlab.model.ImageModel;
import org.springframework.stereotype.Repository;

/**
 * Created by cnlab on 2015/1/24.
 */
@Repository("imageDao")
public class ImageDaoImpl extends BaseDaoImpl<ImageModel> implements IImageDao {

}
