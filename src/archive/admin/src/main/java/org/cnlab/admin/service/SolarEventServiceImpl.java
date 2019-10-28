package org.cnlab.admin.service;

import org.apache.log4j.Logger;
import org.cnlab.admin.model.SolarEventModel;
import org.cnlab.common.QueryModel;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
@Service("solarEventService")
public class SolarEventServiceImpl implements ISolarEventService {
    private static final Logger logger = Logger.getLogger(SolarEventServiceImpl.class);

    @Resource(name = "solarEventDao")
    private org.cnlab.admin.dao.ISolarEventDao solarEventDao;
    /**
     * 0* @param solarEventModel
     *
     * @param solarEventModel
     * @return
     */
    @Override
    public void save(SolarEventModel solarEventModel) throws Exception {
        try {
            solarEventDao.save(solarEventModel);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public void update(SolarEventModel solarEventModel) throws Exception {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("solarEventID", solarEventModel.getSolarEventID());
        try {
            solarEventDao.executeHQL("update SolarEventModel u set u.solarEventName=:solarEventName,u.name=:name,u.modifiedTime=:modifiedTime where u.solarEventID=:solarEventID",map);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public void delete(SolarEventModel solarEventModel) throws Exception {
        try {
            solarEventDao.delete(solarEventModel);
        } catch (Exception e) {
            logger.error("save error" + e.toString());
            throw e;
        }
    }

    @Override
    public List<SolarEventModel> querySolarEvents(QueryModel queryModel) {
       //Map<String, Object> map = new HashMap<String, Object>();
        //map.put("solarEventName", Constants.SUPERADMIN);
        return solarEventDao.find("from SolarEventModel s",queryModel.currentPage,queryModel.pageSize);
    }

    @Override
    public long queryAllSolarEventCounts() {
        return solarEventDao.count(" select count(*) from SolarEventModel");
    }
}
