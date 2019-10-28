package org.cnlab.action;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import org.cnlab.common.QueryModel;
import org.cnlab.model.ImageModel;
import org.cnlab.service.IImageService;
import org.springframework.stereotype.Controller;

import javax.annotation.Resource;
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

    private int pageNumber;
    private int pageSize;

    private String imageID;

    private  ImageModel singleImage;
    private JSONObject result = new JSONObject();

    public String query() throws Exception {
        QueryModel queryModel = new QueryModel();
        queryModel.currentPage = getPageNumber();
        queryModel.pageSize = getPageSize();
        long totalCount = imageService.queryImageCount();
        List<ImageModel> imageModelList = imageService.queryImage(queryModel);
        HashMap<Object, Object> results = new HashMap<Object, Object>();
        if (imageModelList != null) {
            results.put("rows", imageModelList);
        }
        results.put("total", totalCount);
        String rows = JSON.toJSONString(results);

        result = (JSONObject) JSON.parse(rows);

        return "SUCCESS";
    }

    public String query3CleanImage() throws Exception {
        QueryModel queryModel = new QueryModel();
        queryModel.currentPage = 1;
        queryModel.pageSize = 3;
        long totalCount = imageService.queryImageCount();
        List<ImageModel> imageModelList = imageService.queryImage(queryModel);
        HashMap<Object, Object> results = new HashMap<Object, Object>();
        if (imageModelList != null) {
            results.put("rows", imageModelList);
        }
        results.put("total", totalCount);
        String rows = JSON.toJSONString(results);

        result = (JSONObject) JSON.parse(rows);

        return "SUCCESS";
    }

    public String detail() throws Exception {

        singleImage = imageService.querySingleImage(getImageID());

        return "DETAIL";
    }

    public String getImageID() {
        return imageID;
    }

    public void setImageID(String imageID) {
        this.imageID = imageID;
    }

    public JSONObject getResult() {
        return result;
    }

    public void setResult(JSONObject result) {
        this.result = result;
    }

    public int getPageSize() {
        return pageSize;
    }

    public void setPageSize(int pageSize) {
        this.pageSize = pageSize;
    }

    public int getPageNumber() {
        return pageNumber;
    }

    public void setPageNumber(int pageNumber) {
        this.pageNumber = pageNumber;
    }
    public ImageModel getSingleImage() {
        return singleImage;
    }

    public void setSingleImage(ImageModel singleImage) {
        this.singleImage = singleImage;
    }
}
