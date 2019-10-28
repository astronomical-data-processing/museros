package org.cnlab.admin.action;

import com.opensymphony.xwork2.ActionContext;
import org.cnlab.common.MenuItemModel;
import org.springframework.stereotype.Controller;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by cnlab on 2015/1/24.
 */
@Controller
public class IndexAction {
    public List<MenuItemModel> getMenuList() {
        return menuList;
    }

    public void setMenuList(List<MenuItemModel> menuList) {
        this.menuList = menuList;
    }

    List<MenuItemModel> menuList;
    public String toDefault(){
        menuList = new ArrayList<MenuItemModel>();
        MenuItemModel model = new MenuItemModel("subpages/mgrHomePage.jsp","管理主页","icon-mgr-home","mgrHomePage",true,true);
        menuList.add(model);
        model = new MenuItemModel("subpages/webHomePage.jsp","网站主页","icon-web-home","webHomePage",true,false);
        menuList.add(model);
        model = new MenuItemModel("subpages/webImagePage.jsp","图像管理","icon-image-mgr","webImagePage",true,false);
        menuList.add(model);
        model = new MenuItemModel("subpages/webSolarEventPage.jsp","事件管理","icon-image-mgr","webSolarEventPage",true,false);
        menuList.add(model);
        model = new MenuItemModel("subpages/webMoviesPage.jsp","动画管理","icon-movie-mgr","webMoviesPage",true,false);
        menuList.add(model);
        model = new MenuItemModel("subpages/webArticlePage.jsp","文章管理","icon-data-mgr","webArticlePage",true,false);
        menuList.add(model);
        model = new MenuItemModel("subpages/webSearchPage.jsp","搜索管理","icon-search-mgr","webSearchPage",true,false);
        menuList.add(model);
        model = new MenuItemModel("subpages/userManager.jsp","用户管理","icon-user","userManager",true,false);
        menuList.add(model);
        model = new MenuItemModel("subpages/sysConfigPage.jsp","系统配置","icon-sys-conf","sysConfigPage",true,false);
        menuList.add(model);

        ActionContext.getContext().getSession().put("menuList", menuList);
        return "forwardURL";
    }
}
