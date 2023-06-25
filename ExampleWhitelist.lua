---- I recommand using the logger that i added in github to get player infos and hwid to correctly whitelist them --- 
----- load your logger here ----+
local HttpService = game:GetService("HttpService")
local json_data = game:HttpGet("") --- url that you got from your webview, watch tut

local roblox_table = HttpService:JSONDecode(json_data)
local HWID = game:GetService("RbxAnalyticsService"):GetClientId() --- Just Hwid.

local isWhitelisted = false
for _, value in pairs(roblox_table) do
    if value == HWID then
        isWhitelisted = true
        break
    end
end

if isWhitelisted then
   
    print("Found Yet!")
    else if not isWhitelisted then
    print('run free version ')
    end
    end 
--- I just used an hwid whitelist , don't change if you are dumb else change if you are smart ---
 
 
