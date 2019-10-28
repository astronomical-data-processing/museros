package org.cnlab.action;

import com.alibaba.fastjson.JSONObject;
import org.cnlab.common.QueryModel;
import org.cnlab.model.ImageModel;
import org.cnlab.model.IndexPartsModel;
import org.cnlab.service.IImageService;
import org.cnlab.service.IIndexService;
import org.hibernate.internal.util.StringHelper;
import org.springframework.stereotype.Controller;

import javax.annotation.Resource;
import java.util.List;

/**
 * Created by cnlab on 2015/1/24.
 */
@Controller
public class IndexAction {
    private JSONObject result;
    private String ajaxResult;

    @Resource(name = "indexService")
    private IIndexService indexService;

    @Resource(name = "imageService")
    private IImageService imageService;

    private String linkName;

    private IndexPartsModel part;

    public List<ImageModel> getImageModelList() {
        return imageModelList;
    }

    public void setImageModelList(List<ImageModel> imageModelList) {
        this.imageModelList = imageModelList;
    }

    private List<ImageModel> imageModelList;
    private String linkPage;

    public String getLinkPage() {
        return linkPage;
    }

    public void setLinkPage(String linkPage) {
        this.linkPage = linkPage;
    }

    public String toDefault() throws Exception {
        part = new IndexPartsModel();
        QueryModel queryModel = new QueryModel();
        queryModel.currentPage = 1;
        queryModel.pageSize = 3;
        imageModelList = imageService.queryImage(queryModel);
        part.setImageList(imageModelList);
        return "toIndex";
    }

    public String home() throws Exception {
        if (StringHelper.isNotEmpty(getLinkName())) {
            part = new IndexPartsModel();
            QueryModel queryModel = new QueryModel();
            queryModel.currentPage = 1;
            queryModel.pageSize = 3;
            imageModelList = imageService.queryImage(queryModel);
            part.setImageList(imageModelList);
            String linkName = getLinkName().trim();
            if (linkName.equals("menuIndex")) {
                linkPage = "index.jsp";
            }
        }
        return "NAV";
    }

    public String image() {
        if (StringHelper.isNotEmpty(getLinkName())) {
            String linkName = getLinkName().trim();
            if (linkName.equals("menuImage")) {
                linkPage = "image.jsp";
            }
        }
        return "NAV";
    }

    public String research() {
        if (StringHelper.isNotEmpty(getLinkName())) {
            String linkName = getLinkName().trim();
            if (linkName.equals("menuResearch")) {
                linkPage = "research.jsp";
            }
        }
        return "NAV";
    }

    public String movie() {
        if (StringHelper.isNotEmpty(getLinkName())) {
            String linkName = getLinkName().trim();
            if (linkName.equals("menuMovie")) {
                linkPage = "movie.jsp";
            }
        }
        return "NAV";
    }

    public String event() {
        if (StringHelper.isNotEmpty(getLinkName())) {
            String linkName = getLinkName().trim();
            if (linkName.equals("menuEvent")) {
                linkPage = "event.jsp";
            }
        }
        return "NAV";
    }

    public String data() {
        if (StringHelper.isNotEmpty(getLinkName())) {
            String linkName = getLinkName().trim();
            if (linkName.equals("menuData")) {
                linkPage = "data.jsp";
            }
        }
        return "NAV";
    }

    public String about() {
        if (StringHelper.isNotEmpty(getLinkName())) {
            String linkName = getLinkName().trim();
            if (linkName.equals("menuAbout")) {
                linkPage = "about.jsp";
            }
        }
        return "NAV";
    }


    public String getLinkName() {
        return linkName;
    }

    public void setLinkName(String linkName) {
        this.linkName = linkName;
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

    public IndexPartsModel getPart() {
        return part;
    }

    public void setPart(IndexPartsModel part) {
        this.part = part;
    }
}
