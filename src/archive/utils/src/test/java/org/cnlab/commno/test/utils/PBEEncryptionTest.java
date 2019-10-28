package org.cnlab.commno.test.utils;

import junit.framework.TestCase;
import org.cnlab.common.utils.PBEEncryption;

/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/1/30
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
public class PBEEncryptionTest extends TestCase {
    public void testPBE() {
        String str = "PBE";
        String password = "123";

        try {
            byte[] salt = PBEEncryption.getSalt();
            String ciphertext = PBEEncryption.encrypt(str, password, salt);
            TestCase.assertNotSame("79d3980bb2e3f062", ciphertext);
            String plaintext = PBEEncryption.decrypt(ciphertext, password, salt);
            TestCase.assertEquals("PBE", plaintext);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
