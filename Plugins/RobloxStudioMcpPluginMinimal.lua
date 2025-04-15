local HttpService = game:GetService("HttpService")

local relayUrl = "http://localhost:8001"
local mcpUrl = "http://localhost:8002"

-- Test MCP server (server_min.py) health
local healthUrl = mcpUrl .. "/health"
local success, response = pcall(function()
    return HttpService:GetAsync(healthUrl)
end)

if success then
    print("✅ MCP Health OK:", response)
else
    warn("❌ MCP Health FAIL:", response)
end

-- Test generate-script endpoint (server_min.py)
local genUrl = mcpUrl .. "/messages"
local genData = HttpService:JSONEncode({
    type = "generate-script",
    description = "Tạo script chào người chơi"
})

local genResp = HttpService:RequestAsync({
    Url = genUrl,
    Method = "POST",
    Headers = { ["Content-Type"] = "application/json" },
    Body = genData
})

print("Status (generate-script):", genResp.StatusCode)
print("Body (generate-script):", genResp.Body)

if genResp.Success then
    local result = HttpService:JSONDecode(genResp.Body)
    if result.success and result.code then
        print("📝 Lua Script Generated:\n" .. result.code)
    else
        warn("❌ Script generation failed:", result.error)
    end
else
    warn("❌ HTTP request failed:", genResp.StatusCode, genResp.StatusMessage)
end
