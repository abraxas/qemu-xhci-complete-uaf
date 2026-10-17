#!/usr/bin/env bash
set -euo pipefail

QEMU_BIN="${QEMU_BIN:-/opt/qemu/bin/qemu-system-x86_64}"
BIOS_DIR="${QEMU_BIOS_DIR:-/opt/qemu/share/qemu}"

exec "${QEMU_BIN}" \
  -L "${BIOS_DIR}" \
  -machine q35 \
  -accel qtest \
  -cpu qemu64 \
  -smp 1 \
  -m 64M \
  -nodefaults \
  -display none \
  -audio none \
  -qtest tcp:0.0.0.0:18700,server=on,wait=off \
  -qmp tcp:0.0.0.0:18701,server=on,wait=off \
  -d guest_errors \
  -trace enable=usb_xhci_doorbell_write \
  -trace enable=usb_xhci_xfer_async \
  -trace enable=usb_xhci_xfer_success \
  -trace enable=usb_xhci_xfer_error \
  -trace enable=usb_xhci_queue_event \
  -trace enable=usb_xhci_slot_disable \
  -trace enable=usb_xhci_ep_kick \
  -trace enable=usb_xhci_fetch_trb \
  -trace enable=usb_uas_command \
  -trace enable=usb_uas_sense \
  -trace enable=usb_uas_scsi_complete \
  -device qemu-xhci,id=xhci,addr=04.0,p3=0,p2=4 \
  -drive id=drive0,if=none,file=null-co://,file.read-zeroes=on,format=raw \
  -device usb-uas,id=uas,bus=xhci.0 \
  -device scsi-hd,bus=uas.0,scsi-id=0,drive=drive0
