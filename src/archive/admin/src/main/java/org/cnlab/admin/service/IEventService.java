package org.cnlab.admin.service;

import org.cnlab.admin.model.EventModel;
import org.cnlab.common.QueryModel;

import java.util.List;

/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/2/2
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
public interface IEventService {
    List<EventModel> queryEvents(QueryModel queryModel);

    void insertEvent(EventModel event);

    Long queryAllEventCounts();

}
