package org.cnlab.admin.action;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.cnlab.admin.model.ImageModel;
import org.cnlab.admin.service.IImageService;
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
 * @Project: mimage
 * @Author: cnlab
 * @Date: 2015/1/30
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
@Controller
public class ImageAction {
    @Resource(name = "imageService")
    private IImageService imageService;
    private int page;
    private int rows;

    private int ImageID;
    private String ImageName;
    private String Password;
    private String Name;
    private int currentPage;
    private int pageSize;

    private JSONObject result = new JSONObject();
    private String ajaxResult;

    public String add() throws Exception {
        String password = "888888";
        password = CommonHelper.getMD5(password);
        ImageModel imageModel = new ImageModel();
        imageModel.setName(getName());
        String salt = CommonHelper.getUUID();

        SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        Date utilDate = new Date();
        Timestamp sqlDate = new Timestamp(utilDate.getTime());

        imageService.save(imageModel);
        return "SUCCESS";
    }

    public String edit() throws Exception {
        ImageModel imageModel = new ImageModel();
        imageModel.setImageID(getImageID());
        imageModel.setName(getName());

        SimpleDateFormat f = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        Date utilDate = new Date();
        Timestamp sqlDate = new Timestamp(utilDate.getTime());
        imageService.update(imageModel);
        return "SUCCESS";
    }

    public String delete() throws Exception {
        ImageModel imageModel = new ImageModel();
        imageModel.setImageID(getImageID());
        imageService.delete(imageModel);
        result.put("success",true);
        return "SUCCESS";
    }

    public String query() {
        QueryModel queryModel = new QueryModel();
        queryModel.currentPage = page;
        queryModel.pageSize = rows;
        long totalCount = imageService.queryAllImageCounts();
        List<ImageModel> imageModelList = imageService.queryImages(queryModel);
        HashMap<Object, Object> results = new HashMap<Object, Object>();
        if (imageModelList != null) {
            results.put("rows", imageModelList);
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

    public String getImageName() {
        return ImageName;
    }

    public void setImageName(String imageName) {
        ImageName = imageName;
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

    public int getImageID() {
        return ImageID;
    }

    public void setImageID(int imageID) {
        ImageID = imageID;
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
