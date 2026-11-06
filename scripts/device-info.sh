#!/data/data/com.termux/files/usr/bin/bash
set -u

echo "=== A21S CRYPTO MINER — DIAGNOSTIC ==="
echo "Date: $(date)"
echo "Android: $(getprop ro.build.version.release 2>/dev/null || echo unknown)"
echo "SDK: $(getprop ro.build.version.sdk 2>/dev/null || echo unknown)"
echo "Model: $(getprop ro.product.model 2>/dev/null || echo unknown)"
echo "Device: $(getprop ro.product.device 2>/dev/null || echo unknown)"
echo "ABI: $(getprop ro.product.cpu.abi 2>/dev/null || echo unknown)"
echo "Supported ABIs: $(getprop ro.product.cpu.abilist 2>/dev/null || echo unknown)"
echo
echo "--- CPU ---"
if [ -r /proc/cpuinfo ]; then
  grep -E '^(Processor|model name|Hardware|CPU architecture|Features)' /proc/cpuinfo | head -n 12
else
  echo "cpuinfo inaccessible"
fi
echo
echo "--- MEMORY ---"
if [ -r /proc/meminfo ]; then
  grep -E '^(MemTotal|MemAvailable|SwapTotal):' /proc/meminfo
fi
echo
echo "--- BATTERY ---"
if command -v termux-battery-status >/dev/null 2>&1; then
  termux-battery-status
else
  echo "Optionnel : installer Termux:API depuis la même source officielle que Termux, puis pkg install termux-api."
fi
echo
echo "--- STORAGE ---"
df -h "$HOME" 2>/dev/null | tail -n 1
echo
echo "Diagnostic terminé. Aucun minage n'a été lancé."
