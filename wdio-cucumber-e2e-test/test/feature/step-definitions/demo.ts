import { Given, When, Then } from "@wdio/cucumber-framework";

Given(/^Google page is open$/, function (){
    browser.url("https://www.google.com/")
    browser.pause(3000);
});