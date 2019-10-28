package org.cnlab.crawler.framework;

import java.util.HashMap;

/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/2/8
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
public class Rule {
    public Rule(HashMap<String, Object> ruleSet) {
        this.ruleSet = ruleSet;
    }

    public HashMap<String, Object> getRuleSet() {
        return ruleSet;
    }

    public void setRuleSet(HashMap<String, Object> ruleSet) {
        this.ruleSet = ruleSet;
    }

    private HashMap<String, Object> ruleSet;
}
