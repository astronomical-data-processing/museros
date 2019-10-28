package org.cnlab.service;

import org.apache.log4j.Logger;
import org.cnlab.dao.IIndexDao;
import org.cnlab.model.IndexPartsModel;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;


/**
 * Created by cnlab on 2015/1/24.
 */
@Service("indexService")
public class IndexServiceImpl implements IIndexService {
    private static final Logger logger = Logger.getLogger(IndexServiceImpl.class);

    @Resource(name = "indexDao")
    private IIndexDao indexDao;

    @Override
    public List<IndexPartsModel> findAllIndexPartsInfo() {
        logger.info("test");
        return null;
    }
}
