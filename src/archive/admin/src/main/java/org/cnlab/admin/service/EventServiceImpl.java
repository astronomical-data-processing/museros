package org.cnlab.admin.service;

import org.apache.log4j.Logger;
import org.cnlab.admin.model.EventModel;
import org.cnlab.common.QueryModel;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
 * Created by LiuYingBo on 2015/2/1.
 */
@Service("eventService")
public class EventServiceImpl implements IEventService {
    private static final Logger logger = Logger.getLogger(EventServiceImpl.class);

    @Resource(name = "eventDao")
    private org.cnlab.admin.dao.IEventDao eventDao;

    @Override
    public List<EventModel> queryEvents(QueryModel queryModel) {
        return eventDao.find("from EventModel e order by e.eventDateTime desc",queryModel.currentPage,queryModel.pageSize);
    }

    @Override
    public void insertEvent(EventModel event) {
        eventDao.save(event);
    }

    @Override
    public Long queryAllEventCounts() {
        return eventDao.count(" select count(*) from EventModel");
    }
}
