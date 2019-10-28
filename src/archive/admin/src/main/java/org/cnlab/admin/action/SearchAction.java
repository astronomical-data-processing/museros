package org.cnlab.admin.action;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.cnlab.admin.model.SearchModel;
import org.cnlab.admin.service.ISearchService;
import org.cnlab.common.QueryModel;
import org.cnlab.common.utils.CommonHelper;
import org.springframework.stereotype.Controller;

import javax.annotation.Resource;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;


/**
 * @Project: msearch
 * @Author: cnlab
 * @Date: 2015/1/30
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
@Controller
public class SearchAction {
    @Resource(name = "searchService")
    private ISearchService searchService;
    private int page;
    private int rows;

    private int SearchID;
    private String SearchName;
    private String Password;
    private String Name;
    private int currentPage;
    private int pageSize;

    private JSONObject result = new JSONObject();
    private String ajaxResult;

    public String add() throws Exception {
        String password = "888888";
        password = CommonHelper.getMD5(password);
        SearchModel searchModel = new SearchModel();

        SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        Date utilDate = new Date();
        Timestamp sqlDate = new Timestamp(utilDate.getTime());

        searchModel.setCreateTime(sqlDate);
        searchModel.setModifiedTime(sqlDate);
        searchService.save(searchModel);
        return "SUCCESS";
    }

    public String edit() throws Exception {
        SearchModel searchModel = new SearchModel();
        searchModel.setSearchID(getSearchID());

        SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        Date utilDate = new Date();
        Timestamp sqlDate = new Timestamp(utilDate.getTime());
        searchModel.setModifiedTime(sqlDate);
        searchService.update(searchModel);
        return "SUCCESS";
    }

    public String delete() throws Exception {
        SearchModel searchModel = new SearchModel();
        searchModel.setSearchID(getSearchID());
        searchService.delete(searchModel);
        result.put("success",true);
        return "SUCCESS";
    }

    public String query() {
        QueryModel queryModel = new QueryModel();
        queryModel.currentPage = page;
        queryModel.pageSize = rows;
        long totalCount = searchService.queryAllSearchCounts();
        List<SearchModel> searchModelList = searchService.querySearchs(queryModel);
        HashMap<Object, Object> results = new HashMap<Object, Object>();
        if (searchModelList != null) {
            results.put("rows", searchModelList);
        }
        results.put("total", totalCount);
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

    public String getSearchName() {
        return SearchName;
    }

    public void setSearchName(String searchName) {
        SearchName = searchName;
    }

    public String getPassword() {
        return Password;
    }

    public void setPassword(String password) {
        Password = password;
    }


    public int getCurrentPage() {
        return currentPage;
    }

    public void setCurrentPage(int currentPage) {
        this.currentPage = currentPage;
    }

    public int getPageSize() {
        return pageSize;
    }

    public void setPageSize(int pageSize) {
        this.pageSize = pageSize;
    }

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        Name = name;
    }

    public int getSearchID() {
        return SearchID;
    }

    public void setSearchID(int searchID) {
        SearchID = searchID;
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
