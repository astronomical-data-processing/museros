package org.cnlab.admin.dao;

import org.cnlab.admin.model.EventModel;
import org.cnlab.common.dao.impl.BaseDaoImpl;
import org.springframework.stereotype.Repository;

/**
 * Created by cnlab on 2015/1/24.
 */
@Repository("eventDao")
public class EventDaoImpl extends BaseDaoImpl<EventModel> implements IEventDao {

}
