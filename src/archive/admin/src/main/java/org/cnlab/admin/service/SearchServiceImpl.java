package org.cnlab.admin.service;

import org.apache.log4j.Logger;
import org.cnlab.admin.model.SearchModel;
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
@Service("searchService")
public class SearchServiceImpl implements ISearchService {
    private static final Logger logger = Logger.getLogger(LoginServiceImpl.class);

    @Resource(name = "searchDao")
    private org.cnlab.admin.dao.ISearchDao searchDao;
    /**
     * 0* @param searchModel
     *
     * @param searchModel
     * @return
     */
    @Override
    public void save(SearchModel searchModel) throws Exception {
        try {
            searchDao.save(searchModel);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public void update(SearchModel searchModel) throws Exception {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("modifiedTime", searchModel.getModifiedTime());
        map.put("searchID", searchModel.getSearchID());
        try {
            searchDao.executeHQL("update SearchModel u set u.searchName=:searchName,u.name=:name,u.modifiedTime=:modifiedTime where u.searchID=:searchID",map);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public void delete(SearchModel searchModel) throws Exception {
        try {
            searchDao.delete(searchModel);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public List<SearchModel> querySearchs(QueryModel queryModel) {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("searchName", Constants.SUPERADMIN);
        return searchDao.find("from SearchModel u where u.searchName !=:searchName",map,queryModel.currentPage,queryModel.pageSize);
    }

    @Override
    public long queryAllSearchCounts() {
        return searchDao.count(" select count(*) from SearchModel");
    }
}
