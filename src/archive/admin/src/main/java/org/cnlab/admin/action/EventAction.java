package org.cnlab.admin.action;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.cnlab.admin.model.EventModel;
import org.cnlab.common.QueryModel;
import org.springframework.stereotype.Controller;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;

/**
 * Created by cnlab on 2015/1/24.
 */
@Controller
public class EventAction {
    private JSONObject result;
    private String ajaxResult;
    private int page;
    private int rows;
    @Resource(name = "eventService")
    private org.cnlab.admin.service.IEventService eventService;

    public String query() {
        QueryModel queryModel = new QueryModel();
        queryModel.currentPage = page;
        queryModel.pageSize = rows;
        long totalCount = eventService.queryAllEventCounts();
        List<EventModel> eventList = eventService.queryEvents(queryModel);

        HashMap<Object, Object> results = new HashMap<Object, Object>();
        if (eventList != null) {
            results.put("rows", eventList);
        }
        results.put("total",totalCount);
        String rows = JSON.toJSONString(results);
        result = (JSONObject) JSON.parse(rows);
        return "SUCCESS";
    }

    public JSONObject getResult() {
        return result;
    }

    public void setResult(JSONObject result) {
        this.result = result;
    }

    public String getAjaxResult() {
        return ajaxResult;
    }

    public void setAjaxResult(String ajaxResult) {
        this.ajaxResult = ajaxResult;
    }

    public int getPage() {
        return page;
    }

    public void setPage(int page) {
        this.page = page;
    }

    public int getRows() {
        return rows;
    }

    public void setRows(int rows) {
        this.rows = rows;
    }

}
